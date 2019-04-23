import datetime
import typing

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText


def send_alert(
    server: str,
    username: str,
    password: str,
    sender: str,
    recipients: typing.List[str],
    month_ratio: float,
    usage_ratio: float,
):
    now = datetime.datetime.now()
    date_string = now.strftime("%Y/%m/%d")

    # typical values for text_subtype are plain, html, xml
    text_subtype = "plain"

    content = f"""\
    Usage alert on {date_string}

    You are {usage_ratio*100}% through your usage cap, but the month is only {round(month_ratio*100, 2)}% done.
    """

    subject = "Internet Usage Alert - %s" % date_string

    msg = MIMEText(content, text_subtype)
    msg["Subject"] = subject
    msg["From"] = sender

    conn = SMTP(server)
    conn.set_debuglevel(False)
    conn.login(username, password)

    try:
        conn.sendmail(sender, recipients, msg.as_string())
    finally:
        conn.quit()


def send_debug(
    server: str,
    username: str,
    password: str,
    sender: str,
    recipients: typing.List[str],
    exc: Exception,
):
    now = datetime.datetime.now()
    date_string = now.strftime("%Y/%m/%d")

    # typical values for text_subtype are plain, html, xml
    text_subtype = "plain"

    content = f"""\
    Exception occured in Internet Usage Alerter on {date_string}

    {exc}
    """

    subject = "Exception - Internet Usage Alert - %s" % date_string

    msg = MIMEText(content, text_subtype)
    msg["Subject"] = subject
    msg["From"] = sender

    conn = SMTP(server)
    conn.set_debuglevel(False)
    conn.login(username, password)

    try:
        conn.sendmail(sender, recipients, msg.as_string())
    finally:
        conn.quit()
