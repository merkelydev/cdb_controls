from pipe import BitbucketPipe, schema

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_required_env_vars(capsys, mocker):
    # BITBUCKET_WORKSPACE probably should be required, but None ends up in the url
    # BITBUCKET_REPO_SLUG probably should be required, but None ends up in the url
    # CDB_TEST_RESULTS_DIR has a default, '/data/junit/' but this is _not_ checked
    # resulting in message:
    #   "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 0 test suites"
    bitbucket_commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    env = {
        "CDB_COMMAND": "control_junit",
        "CDB_PIPELINE_DEFINITION": "tests/data/pipefile.json",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
        "CDB_ARTIFACT_SHA": "aacdaef69c676c2466571d3211110d559ccc2032b258fc5e73f99a103db462ee",
        "BITBUCKET_COMMIT": bitbucket_commit,
        "BITBUCKET_BUILD_NUMBER": "127",
    }
    set_env_vars = {
        'CDB_ARTIFACT_GIT_URL': 'https://bitbucket.org/None/None/commits/' + bitbucket_commit,
        'CDB_ARTIFACT_GIT_COMMIT': bitbucket_commit,
        'CDB_BUILD_NUMBER': '127',
        'CDB_CI_BUILD_URL': 'https://bitbucket.org/None/None/addon/pipelines/home#!/results/127'
    }
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        pipe.run()
    verify_approval(capsys)


def test_intended_env_vars(capsys, mocker):
    # BITBUCKET_COMMIT and BITBUCKET_BUILD_NUMBER are required
    # If they are not set the code tries to set an env-var to none
    bitbucket_commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    env = {
        "CDB_COMMAND": "control_junit",
        "CDB_PIPELINE_DEFINITION": "tests/data/pipefile.json",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
        "CDB_ARTIFACT_SHA": "aacdaef69c676c2466571d3211110d559ccc2032b258fc5e73f99a103db462ee",
        "BITBUCKET_COMMIT": bitbucket_commit,
        "BITBUCKET_BUILD_NUMBER": "127",
        "BITBUCKET_WORKSPACE": "acme",
        "BITBUCKET_REPO_SLUG": "road-runner"
    }
    set_env_vars = {
        'CDB_ARTIFACT_GIT_URL': 'https://bitbucket.org/acme/road-runner/commits/' + bitbucket_commit,
        'CDB_ARTIFACT_GIT_COMMIT': bitbucket_commit,
        'CDB_BUILD_NUMBER': '127',
        'CDB_CI_BUILD_URL': 'https://bitbucket.org/acme/road-runner/addon/pipelines/home#!/results/127'
    }
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        pipe.run()
    verify_approval(capsys)

