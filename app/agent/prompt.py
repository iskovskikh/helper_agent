from settings.config import config


def get_system_prompt():
    return config.prompt.system_prompt
