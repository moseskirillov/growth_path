import logging


def logging_init():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    database_logger = logging.getLogger('peewee.database')
    database_logger.addHandler(logging.StreamHandler())
    database_logger.setLevel(logging.DEBUG)
