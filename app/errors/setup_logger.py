import logging

logging.basicConfig()
logger = logging.getLogger("sqlalchemy")
logger.setLevel(logging.INFO)
handler = logging.FileHandler('app/errors/db_info.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
