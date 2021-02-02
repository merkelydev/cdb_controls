from commands import command_processor, Context
from tests.utils import *


def test_raises_when_api_token_not_set(capsys):
    ev = core_env_vars()
    ev.pop("MERKELY_API_TOKEN")

    with dry_run(ev) as env:
        with ScopedFileCopier("/app/tests/data/Merkelypipe.json", "/Merkelypipe.json"):
            status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def test_raises_when_api_token_is_empty_string(capsys):
    ev = core_env_vars()
    ev["MERKELY_API_TOKEN"] = ""

    with dry_run(ev) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)