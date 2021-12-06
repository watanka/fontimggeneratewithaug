import logging
import logging.config
import sys


def createLogger(logger_name):
    # Logger Setting
    return logging.getLogger(logger_name)


def configure_log() -> None:
    # default logging to stdout
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s][%(name)s][%(levelname)s] - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
    # f = ContextFilter()
    # root.addFilter(f)


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    UUID = "UUID"
    DOCNAME = "MAIN"

    def filter(self, record):
        record.uuid = ContextFilter.UUID
        record.docname = ContextFilter.DOCNAME
        return True
