from python_ntfy import NtfyClient
from python_ntfy import MessageSendError
import os
import db
from exceptions import EbaiException


def init():
    global c
    c = NtfyClient(server=os.getenv("NTFY_SERVER"), topic=os.getenv("NTFY_TOPIC"), auth=(os.getenv("NTFY_USER"), os.getenv("NTFY_PASS")))


def send(msg):
    try:
        c.send(msg)
    except MessageSendError as e:
        err_id = EbaiException.NtfyException
        if db.has_error(err_id):
            db.insert_error(err_id, e.message)

            # this might fail too, but it won't get executed again because of the check above
            send_err(err_id, e.message)


def send_err(id, msg):
    send(f"Error {id}: {msg}")
