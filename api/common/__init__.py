
def get_bool_env(env_var_name: str, default: str = "0") -> bool:
    from os import getenv
    return getenv(env_var_name, default).lower() in ("1", "true", "yes", "on")


def get_database_config(base_dir):
    from os import getenv
    if getenv("USE_POSTGRES", "false").lower() == "true":
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": getenv("POSTGRES_DB"),
            "USER": getenv("POSTGRES_USER"),
            "PASSWORD": getenv("POSTGRES_PASSWORD"),
            "HOST": getenv("POSTGRES_HOST"),
            "PORT": getenv("POSTGRES_PORT"),
        }
    else:
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": base_dir / "db.sqlite3",
        }

