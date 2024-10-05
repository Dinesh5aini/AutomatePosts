import logging
import os
from datetime import datetime

log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = datetime.now().strftime('%m_%d_%Y_%H_%M_%S') + '.log'
log_file_path = os.path.join(log_dir, log_file)

logging.basicConfig(
    filename=log_file_path,
    format='[%(asctime)s] %(name)s:%(lineno)d %(levelname)s - %(message)s',
    level=logging.INFO
)