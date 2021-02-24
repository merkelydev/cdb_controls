from abc import ABC
from collections import namedtuple
from env_vars import *


class Command(ABC):
    """
    Abstract Base Class for all merkely/change commands.
    """
    def __init__(self, external):
        self._external = external

    def __call__(self):  # pragma: no cover
        raise NotImplementedError(self.name)

    # - - - - - - - - - - - - - - - - - - - - -
    # Merkelypipe.json

    @property
    def merkelypipe(self):
        return self._external.merkelypipe

    # - - - - - - - - - - - - - - - - - - - - -
    # All env-vars

    @property
    def env_vars(self):
        names = self._env_var_names
        objects = [getattr(self, name) for name in names]
        return namedtuple('EnvVars', tuple(names))(*objects)

    # - - - - - - - - - - - - - - - - - - - - -
    # Common env-vars

    @property
    def api_token(self):
        notes = "Your API token for Merkely."
        return self._required_env_var("MERKELY_API_TOKEN", notes)

    @property
    def ci_build_url(self):
        return CIBuildUrlEnvVar(self.env)

    @property
    def fingerprint(self):
        return FingerprintEnvVar(self._external)

    @property
    def host(self):
        return HostEnvVar(self.env)

    @property
    def name(self):
        notes = "The Merkely command to execute."
        return self._required_env_var("MERKELY_COMMAND", notes)

    @property
    def user_data(self):
        return UserDataEnvVar(self._external)

    # - - - - - - - - - - - - - - - - - - - - -

    @property
    def is_compliant(self):
        notes = "TRUE if the artifact is considered compliant from you build process."
        return self._required_env_var('MERKELY_IS_COMPLIANT', notes)

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")

    # - - - - - - - - - - - - - - - - - - - - -

    @property
    def env(self):
        return self._external.env

    def _required_env_var(self, name, notes):
        return RequiredEnvVar(self.env, name, notes)

    def _static_defaulted_env_var(self, name, default, notes):
        return StaticDefaultedEnvVar(self.env, name, default, notes)

    def _defaulted_env_var(self, name, notes):
        return DefaultedEnvVar(self.env, name, notes)

    # - - - - - - - - - - - - - - - - - - - - -

    def invocation(self, type):
        def env(var):
            if var.name == "MERKELY_COMMAND":
                value = var.value
            else:
                value = '"' + "${" + var.name + "}" + '"'
            return f'    --env {var.name}={value} \\\n'

        invocation_string = "docker run \\\n"
        for name in self._env_var_names:
            var = getattr(self, name)
            if type == 'full':
                invocation_string += env(var)
            if type == 'minimum' and var.is_required:
                invocation_string += env(var)

        invocation_string += "    --rm \\\n"
        for mount in self._volume_mounts:
            invocation_string += f"    --volume {mount} \\\n"
        invocation_string += "    --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \\\n"
        invocation_string += "    merkely/change"
        return invocation_string

    @property
    def _env_var_names(self):  # pragma: no cover
        raise NotImplementedError(self.name)

    @property
    def _volume_mounts(self):  # pragma: no cover
        raise NotImplementedError(self.name)
