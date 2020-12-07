import logging


LOG_FILENAME = "logfile.log"
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.info('Forecastiong Job Started...')
logging.debug('abc method started...')