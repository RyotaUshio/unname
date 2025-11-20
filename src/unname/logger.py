import logging

# Source - https://stackoverflow.com/a/56944256
# Posted by Sergey Pleshakov, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
# Further modified by Ryota Ushio to fix type errors


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;20m'
    yellow = '\x1b[33;20m'
    red = '\x1b[31;20m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    template = '%(levelname)s: %(message)s'

    FORMATS = {
        logging.DEBUG: grey + template + reset,
        logging.INFO: grey + template + reset,
        logging.WARNING: yellow + template + reset,
        logging.ERROR: red + template + reset,
        logging.CRITICAL: bold_red + template + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger('unname')
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)
