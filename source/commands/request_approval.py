from commands import Command
from docs import *
from env_vars import *
from lib.api_schema import ApiSchema
from lib.git import repo_at, list_commits_between


class RequestApproval(Command):

    def doc_summary(self):
        return "Request an approval in Merkely."

    def doc_volume_mounts(self):
        return [
            "${PWD}:/src",
            "/var/run/docker.sock:/var/run/docker.sock"
        ]

    def doc_ref(self):
        return {
            'docker': (docker_change_makefile_line_ref, 'merkely_request_approval:'),
            'github': (github_loan_calculator_request_approval_line_ref, 'MERKELY_COMMAND: request_approval'),
            'bitbucket': (bitbucket_loan_calculator_line_ref, 'MERKELY_COMMAND: request_approval'),
        }

    def __call__(self):
        url = ApiSchema.url_for_approvals(self.host.value, self.merkelypipe)
        commit_list = list_commits_between(repo_at(self.src_repo_root.value),
                                           self.newest_src_commitish.value,
                                           self.oldest_src_commitish.value)
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "description": self.description.value,
            "src_commit_list": commit_list,
            "user_data": self.user_data.value,
            "approvals": []
        }
        return 'POST', url, payload, None

    @property
    def description(self):
        return DescriptionEnvVar(self.env)

    @property
    def oldest_src_commitish(self):
        return OldestSrcCommitishEnvVar(self.env)

    @property
    def newest_src_commitish(self):
        return NewestSrcCommitishEnvVar(self.env)

    @property
    def src_repo_root(self):
        return SrcRepoRootEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'oldest_src_commitish',
            'newest_src_commitish',
            'description',
            'src_repo_root',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
            'dry_run'
        ]


class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DESCRIPTION")

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"Approval requested by ${{ github.actor }} on github"'
        if ci_name == 'bitbucket':
            return True, '"Approval requested on bitbucket"'
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return f"A description for the approval request."
