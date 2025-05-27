
def get_bool_env(env_var_name: str, default: str = "0") -> bool:
    from os import getenv
    return getenv(env_var_name, default).lower() in ("1", "true", "yes", "on")
