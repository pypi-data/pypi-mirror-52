import logging
import os

import dotenv

from core import utils


def set_config(**kwargs):
    """
    :param kwargs:
    :return:
    """
    log_level = logging.DEBUG
    log_filename = kwargs.get('logging_filename', None)
    log_format = '%(asctime)-15s %(levelname)s [%(name)s] [in %(pathname)-10s:%(funcName)-20s:%(lineno)-5d]: ' \
                 '%(message)s'
    logging.basicConfig(
        format=log_format,
        filename=log_filename,
        level=log_level,
        filemode='w',
    )


if __name__ == '__main__':
    dotenv.load_dotenv(dotenv_path=os.getenv('ENV_FILE'))
    set_config()
    logging.info('starting...')
    host_ = os.getenv('IMAP_HOST')
    port_ = os.getenv('IMAP_PORT')
    login_ = os.getenv('EMAIL_LOGIN')
    password_ = os.getenv('EMAIL_PASSWORD')
    is_clean = os.getenv('CLEAN')
    logging.info(f'envs is extracted:\tIMAP_HOST={host_}\tIMAP_PORT={port_}\tEMAIL_LOGIN={login_}\t'
                 f'EMAIL_PASSWORD={password_}\tCLEAN={is_clean}')
    assert is_clean == 'YES', 'CLEAN environment variable is not set as YES'
    utils.clean_email(host_, port_, login_, password_)
