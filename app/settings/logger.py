from settings.config import Config


def get_logger_config(config: Config):
    config.log.path.mkdir(parents=True, exist_ok=True)

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default_console_format": {
                "format": config.log.console_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": True,
            },
            "default_file_format": {
                "format": config.log.file_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": False,
            },
        },
        "handlers": {
            "console_handler": {
                "formatter": "default_console_format",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file_handler": {
                "formatter": "default_file_format",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": config.log.path / "app.log",
                "maxBytes": 1024 * 1024 * 1,  # = 1MB
                "backupCount": 10,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console_handler", ],
                "level": "DEBUG",
                "propagate": True,
            },
            # "httpx": {
            #     "handlers": ["console_handler", "file_handler"],
            #     "level": "WARNING",
            # },
            # "httpcore": {
            #     "handlers": ["console_handler", "file_handler"],
            #     "level": "WARNING",
            # },
            # "gigachat": {
            #     "handlers": ["console_handler", "file_handler"],
            #     "level": "WARNING",
            # },
            # "urllib3": {
            #     "handlers": ["console_handler", "file_handler"],
            #     # "level": "WARNING",
            #     "level": "INFO",
            # },
        },
    }
