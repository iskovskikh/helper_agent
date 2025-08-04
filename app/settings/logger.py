
import logging.config

logging_config = {
    "version": 1,
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
            "handlers": ["console",],
            "propagate": False,  # Не передавать логи родительским логгерам
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