import contextlib
import fnmatch
import os
import pathlib
import shlex
import shutil
import site
import subprocess
import sys
import tempfile
import textwrap
import typing as t

import attr
import hyperlink
import pkg_resources
import pyrsistent
import requests
import requirements

from . import results
from . import satests


os.environ.pop("TOXENV", None)


@attr.dataclass(frozen=True)
class Dependent:
    repository: str
    toxenv_glob: str


@attr.dataclass(frozen=True)
class Project:
    test_command: t.Sequence[str] = attr.ib(
        default=["tox"], converter=pyrsistent.freeze
    )


@attr.dataclass(frozen=True)
class GitRepo:
    url: hyperlink.URL = attr.ib(converter=hyperlink.URL.from_text)
    project: Project


@contextlib.contextmanager
def install_hooks(module: str):
    """

    Args:
        module: The module to insert.

    """
    path = pathlib.Path(site.USER_SITE) / "usercustomize.py"
    try:
        original = path.read_text()
    except FileNotFoundError:
        original = None

    module = repr(str(module))
    text = textwrap.dedent(
        f"""\
    import os
    import sys

    def hook(*args):
        with open('/tmp/checkon/' + str(os.getpid())) as f:
            f.write(str(args))

    sys.excepthook = hook


    sys.path.insert(0, {module})
    """
    )
    path.write_text(text)
    try:
        yield
    finally:
        pass
        if original is None:
            path.unlink()
        else:
            path.write_text(original)


def get_dependents(pypi_name, api_key, limit):

    url = f"https://libraries.io/api/pypi/{pypi_name}/dependents?api_key={api_key}&per_page={limit}"
    response = requests.get(url)

    return [
        Dependent(project["repository_url"], "*")
        for project in response.json()
        if project["repository_url"]
    ]


def resolve_inject(inject):
    """Resolve local requirements path."""
    try:
        req = list(requirements.parse(inject))[0]
    except pkg_resources.RequirementParseError:
        req = list(requirements.parse("-e" + str(inject)))[0]
    if req.path and not req.path.startswith("git+"):
        return str(pathlib.Path(req.path).resolve())
    return inject


def run_toxenv(dependent: Dependent, toxenv: str, inject: str):
    # TODO Refactor to fill this out.
    ...


def run_one(dependent, inject: str, log_file):

    results_dir = pathlib.Path(tempfile.TemporaryDirectory().name)
    results_dir.mkdir(exist_ok=True, parents=True)

    clone_tempdir = pathlib.Path(tempfile.TemporaryDirectory().name)
    subprocess.run(
        ["git", "clone", dependent.repository, str(clone_tempdir)],
        check=True,
        stdout=log_file,
        stderr=log_file,
    )

    rev_hash = (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=clone_tempdir)
        .decode()
        .strip()
    )

    project_tempdir = pathlib.Path(".checkon/" + str(rev_hash))
    project_tempdir.parent.mkdir(exist_ok=True)

    tox = [sys.executable, "-m", "tox"]

    if not project_tempdir.exists():
        shutil.move(clone_tempdir, project_tempdir)

    # Get environment names.
    envnames = (
        subprocess.run(
            tox + ["-l"],
            cwd=str(project_tempdir),
            capture_output=True,
            check=True,
            env={k: v for k, v in os.environ.items() if k != "TOXENV"},
        )
        .stdout.decode()
        .splitlines()
    )
    envnames = [
        name for name in envnames if fnmatch.fnmatch(name, dependent.toxenv_glob)
    ]

    for envname in envnames:

        # Create the envs and install deps.
        subprocess.run(
            tox
            + [
                "-e",
                envname,
                "--notest",
                "-c",
                str(project_tempdir.resolve()),
                "--result-json",
                str(results_dir / "tox_install.json"),
            ],
            cwd=str(project_tempdir),
            check=False,
            env={k: v for k, v in os.environ.items() if k != "TOXENV"},
            stdout=log_file,
            stderr=log_file,
        )

        # Install the `trial` patch.
        # TODO Put the original `trial` back afterwards.
        subprocess.run(
            tox
            + ["-e", envname, "--run-command", "python -m pip install checkon-trial"],
            cwd=str(project_tempdir),
            env={k: v for k, v in os.environ.items() if k != "TOXENV"},
            stdout=log_file,
            stderr=log_file,
        )

        # TODO Install the `unittest` patch by adding a pth or PYTHONPATH replacing `unittest` on sys.path.

        # Install the injection into each venv
        subprocess.run(
            tox
            + [
                "-e",
                envname,
                "--run-command",
                "python -m pip install --force " + shlex.quote(str(inject)),
            ],
            cwd=str(project_tempdir),
            env={k: v for k, v in os.environ.items() if k != "TOXENV"},
            stdout=log_file,
            stderr=log_file,
        )

        # Run the environment.
        output_dir = results_dir / envname
        output_dir.mkdir(exist_ok=True, parents=True)
        test_output_file = output_dir / f"test_{envname}.xml"
        tox_output_file = output_dir / f"tox_{envname}.json"
        env = {
            "TOX_TESTENV_PASSENV": "PYTEST_ADDOPTS JUNITXML_PATH",
            "PYTEST_ADDOPTS": f"--tb=long --junitxml={test_output_file}",
            "JUNITXML_PATH": test_output_file,
            **os.environ,
        }
        env.pop("TOXENV", None)
        subprocess.run(
            tox + ["-e", envname, "--result-json", str(tox_output_file), "-e", envname],
            cwd=str(project_tempdir),
            check=False,
            env=env,
            stdout=log_file,
            stderr=log_file,
        )

    return results.AppSuiteRun(
        injected=inject,
        dependent_result=results.DependentResult.from_dir(
            output_dir=results_dir, url=dependent.repository
        ),
    )


def run_many(dependents: t.List[Dependent], inject: str, log_file):
    inject = resolve_inject(inject)
    url_to_res = {}

    for dependent in dependents:
        url_to_res[dependent.repository] = run_one(
            dependent, inject=inject, log_file=log_file
        )

    return url_to_res


def test(
    dependents: t.List[Dependent],
    inject_new: t.Sequence[str],
    inject_base: str,
    log_file,
):
    db = satests.Database.from_string("sqlite:///:memory:", echo=False)
    db.init()

    for lib in list(inject_new) + [inject_base]:
        for result in run_many(dependents, lib, log_file=log_file).values():
            satests.insert_result(db, result)

    if inject_new and inject_base:
        query = COMPARISON_QUERY
    else:
        query = SIMPLE_QUERY

    out = [
        dict(zip(d.keys(), d.values()))
        for d in (db.engine.execute(query, (inject_base,) or inject_new))
    ]
    return out


SIMPLE_QUERY = """
SELECT
    ter.envname,
    tr.application,
    tc.classname,
    tc.name,
    tc.line,
    tr.provider,
    fo.message,
    fo.text

FROM test_case_run tcr
LEFT JOIN test_failure tf ON tcr.test_failure_id = tf.test_failure_id
LEFT JOIN test_suite_run tsr ON tsr.test_suite_run_id = tcr.test_suite_run_id
LEFT JOIN toxenv_run ter ON ter.test_suite_run_id = tsr.test_suite_run_id
LEFT JOIN tox_run tr ON tr.tox_run_id = ter.tox_run_id
LEFT JOIN failure_output fo ON tf.failure_output_id = fo.failure_output_id
LEFT JOIN test_case tc ON tcr.test_case_id = tc.test_case_id
ORDER BY ter.envname, tr.application, tc.classname, tc.line, tc.name, tr.provider
"""


COMPARISON_QUERY = """
       WITH result AS (
       SELECT
           ter.envname,
           tr.application,
           tc.classname,
           tc.name,
           tc.line,
           tr.provider,
           fo.message,
           fo.text
       FROM test_case_run tcr
       LEFT JOIN test_failure tf ON tcr.test_failure_id = tf.test_failure_id
       LEFT JOIN test_suite_run tsr ON tsr.test_suite_run_id = tcr.test_suite_run_id
       LEFT JOIN toxenv_run ter ON ter.test_suite_run_id = tsr.test_suite_run_id
       LEFT JOIN tox_run tr ON tr.tox_run_id = ter.tox_run_id
       LEFT JOIN failure_output fo ON tf.failure_output_id = fo.failure_output_id
       LEFT JOIN test_case tc ON tcr.test_case_id = tc.test_case_id
       ORDER BY ter.envname, tr.application, tc.classname, tc.line, tc.name, tr.provider
       )
       SELECT new.* FROM result base
       LEFT JOIN result new ON base.name=new.name AND base.classname=new.classname and base.line=new.line
       WHERE base.provider = ?
       AND base.message is null and base.text is null
       AND base.provider != new.provider
       AND new.message is not null

"""
