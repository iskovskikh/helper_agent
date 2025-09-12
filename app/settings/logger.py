import logging.config

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s %(levelname)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(levelname)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            # "formatter": "default",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        # "file": {
        #     "class": "logging.FileHandler",
        #     "level": "DEBUG",
        #     "formatter": "default",
        #     "filename": "app.log",
        #     "mode": "a",  # 'a' - append, 'w' - overwrite
        # },
        # "rotating_file": {
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "level": "INFO",
        #     "formatter": "default",
        #     "filename": "app_rotating.log",
        #     "maxBytes": 5 * 1024 * 1024,  # 5 MB
        #     "backupCount": 3,
        #     "encoding": "utf-8",
        # },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": True,  # Не передавать логи родительским логгерам
        },
        # "default": {
        #     "level": "DEBUG",
        #     "handlers": ["console", "file", "rotating_file"],
        #     "propagate": False,  # Не передавать логи родительским логгерам
        # },
        # "requests": {  # Пример настройки для стороннего логгера (например, библиотеки requests)
        #     "level": "WARNING",
        #     "handlers": ["console"],
        #     "propagate": False,
        # },
    },
    "root": {  # Настройки корневого логгера (если не найден конкретный логгер)
        "level": "DEBUG",
        "handlers": ["console"],
    },
}


def init_logger():
    logging.config.dictConfig(logging_config)


# from settings.config import Config
#
#
# def get_logger_config(config: Config):
#     config.log.path.mkdir(parents=True, exist_ok=True)
#
#     return {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "default_console_format": {
#                 "format": config.log.console_format,
#                 "datefmt": "%Y-%m-%d %H:%M:%S",
#                 "use_colors": True,
#             },
#             "default_file_format": {
#                 "format": config.log.file_format,
#                 "datefmt": "%Y-%m-%d %H:%M:%S",
#                 "use_colors": False,
#             },
#         },
#         "handlers": {
#             "console_handler": {
#                 "formatter": "default_console_format",
#                 "class": "logging.StreamHandler",
#                 "stream": "ext://sys.stdout",
#             },
#             "file_handler": {
#                 "formatter": "default_file_format",
#                 "class": "logging.handlers.RotatingFileHandler",
#                 "filename": config.log.path / "app.log",
#                 "maxBytes": 1024 * 1024 * 1,  # = 1MB
#                 "backupCount": 10,
#                 "encoding": "utf8",
#             },
#         },
#         "loggers": {
#             "": {
#                 "handlers": ["console_handler", ],
#                 "level": "DEBUG",
#                 "propagate": True,
#             },
#             # "httpx": {
#             #     "handlers": ["console_handler", "file_handler"],
#             #     "level": "WARNING",
#             # },
#             # "httpcore": {
#             #     "handlers": ["console_handler", "file_handler"],
#             #     "level": "WARNING",
#             # },
#             # "gigachat": {
#             #     "handlers": ["console_handler", "file_handler"],
#             #     "level": "WARNING",
#             # },
#             # "urllib3": {
#             #     "handlers": ["console_handler", "file_handler"],
#             #     # "level": "WARNING",
#             #     "level": "INFO",
#             # },
#         },
#     }
