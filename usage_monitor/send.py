import typing

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText


def send_alert(
    server: str, username: str, password: str, sender: str, recipients: typing.List[str], month_ratio: float, usage_ratio: float,
):
    # typical values for text_subtype are plain, html, xml
    text_subtype = "plain"

    content = """\
    Test message
    """

    subject = "Sent from Python"

    msg = MIMEText(content, text_subtype)
    msg["Subject"] = subject
    msg["From"] = sender  # some SMTP servers will do this automatically, not all

    conn = SMTP(server)
    conn.set_debuglevel(False)
    conn.login(username, password)

    try:
        conn.sendmail(sender, recipients, msg)
    finally:
        conn.quit()
