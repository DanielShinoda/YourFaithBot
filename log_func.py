import logging


def log(message, level):
    logging.basicConfig(filename='output.csv',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG)

    if level.upper() == "DEBUG":
        logging.debug(message)
    if level.upper() == "INFO":
        logging.info(message)
    if level.upper() == "WARNING":
        logging.warning(message)
    if level.upper() == "ERROR":
        logging.error(message)
    if level.upper() == "CRITICAL":
        logging.critical(message)
