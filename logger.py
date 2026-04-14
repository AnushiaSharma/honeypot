import logging

logging.basicConfig(
    filename='attack.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def log_attack(message):
    logging.info(message)