from cdb.control_junit import control_junit
import docker

from pytest import raises
from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval, auto_reading


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    env = {
        "CDB_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_EVIDENCE_TYPE": "unit_test",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1456",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    env = {
        "CDB_API_TOKEN": "7199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:3.4",
        "CDB_EVIDENCE_TYPE": "coverage",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1457",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        sha = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_all_env_vars(capsys, mocker):
    # Uses CDB_EVIDENCE_TYPE == /data/test/junit
    # This dir does not exist, but is not checked. Results in message
    # "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 0 test suites"
    env = {
        "CDB_HOST": "http://test.compliancedb.com",
        "CDB_API_TOKEN": "7199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_TEST_RESULTS_DIR": "/data/test/junit",
        "CDB_EVIDENCE_TYPE": "coverage",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1457",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_no_env_vars_raises_DockerException(capsys):
    env = CDB_DRY_RUN
    set_env_vars = {}
    with AutoEnvVars(env, set_env_vars), raises(docker.errors.DockerException), auto_reading(capsys):
        control_junit("tests/integration/test-pipefile.json")



