import logging
import logging.config

import settings

logging.config.dictConfig(settings.LOGGING)

getLogger = logging.getLogger
