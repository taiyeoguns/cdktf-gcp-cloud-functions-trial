from cdktf import App
from decouple import config

from config import (
    APP_NAME,
    Env,
    dev_environment_data,
    prod_environment_data,
    staging_environment_data,
)
from stacks.my_stack import MyStack

env = config("ENV", str(Env.DEV))

env_stack = {
    str(Env.DEV): dev_environment_data,
    str(Env.STAGING): staging_environment_data,
    str(Env.PRODUCTION): prod_environment_data,
}

env_data = env_stack.get(env)

if not env_data:
    raise ValueError(f"Environment {env} not supported. Check config")

app = App()
MyStack(app, env_data.env_name(APP_NAME), env_data=env_data)

app.synth()
