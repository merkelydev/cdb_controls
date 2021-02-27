from commands import Command, External


def test_invocation_strings():
    env = {"MERKELY_COMMAND": "unused"}
    external = External(env=env)
    for klass in Command.all().values():
        command = klass(external)
        assert len(command.invocation('full', 'github')) > 0
        assert len(command.invocation('minimum', 'bitbucket')) > 0


