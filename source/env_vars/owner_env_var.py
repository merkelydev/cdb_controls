from env_vars import RequiredEnvVar

NOTES = "Your user/organization name in Merkely."


class OwnerEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_OWNER", NOTES)

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ env.MERKELY_OWNER }}"
        if ci_name == 'bitbucket':
            return True, "${MERKELY_OWNER}"
        return False, ""

