import imaplib
import logging


def clean_email(host, port, login, password):
    """
    clean_email cleans email by next params. Before execution, you can configurate standart python logger, then you get
    logging

    :param host:
    :param port:
    :param login:
    :param password:
    :return: None
    """
    logging.info('connect to server')
    box = imaplib.IMAP4_SSL(host, port)
    logging.info('log-in')
    status, resp = box.login(login, password)
    assert status == 'OK', f'status is not OK. status: {status}. resp: {resp}'
    logging.info('get list folders')
    status, resp = box.list()
    assert status == 'OK', f'request list of email\'s folders returns not OK status: {status}. resp: {resp}'
    folders = list(map(lambda f: str(f).split(' ')[-1][1:-2], resp))
    for folder in folders:
        logging.info(f'folder: {folder}')
        status, resp = box.select(folder)
        assert status == 'OK', f'request select folder returns not OK status: {status}. resp: {resp}'
        status, resp = box.search(None, 'ALL')
        assert status == 'OK', f'request select folder returns not OK status: {status}. resp: {resp}'
        for num in resp[0].split():
            status, resp = box.store(num, '+FLAGS', '\\Deleted')
            assert status == 'OK', f'request store returns not OK status: {status}. resp: {resp}'
        status, resp = box.expunge()
        assert status == 'OK', f'request expunge returns not OK status: {status}. resp: {resp}'
    status, resp = box.close()
    assert status == 'OK', f'request close returns not OK status: {status}. resp: {resp}'
    status, resp = box.logout()
    assert status == 'BYE', f'request logout returns not OK status: {status}. resp: {resp}'
    logging.info('finished')
