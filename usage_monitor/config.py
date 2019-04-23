import configparser
import enum
import os
import typing

if typing.TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

class UsageConfig(typing.NamedTuple):
    driver: typing.Optional['WebDriver']

    xplornet_username: str
    xplornet_password: str

    email_server: str
    email_username: str
    email_password: str
    email_sender: str
    email_recipients: typing.List[str]

    debug: bool
    debug_recipients: typing.List[str]

    @staticmethod
    def from_file(filename: str, *, driver=None) -> "UsageConfig":
        config = configparser.ConfigParser()
        config.read(filename)

        return UsageConfig(
            driver=driver,
            xplornet_username=config["xplornet"]["username"],
            xplornet_password=config["xplornet"]["password"],
            email_server=config["email"]["server"],
            email_username=config["email"]["username"],
            email_password=config["email"]["password"],
            email_sender=config["email"]["sender"],
            email_recipients=[
                email.strip() for email in config["email"]["recipients"].split(",")
            ],
            debug=config.getboolean("debug", "debug", fallback=False),
            debug_recipients=[
                email.strip()
                for email in config.get(
                    "debug", "recipients", fallback=config["email"]["recipients"]
                ).split(",")
            ],
        )

    @staticmethod
    def from_env(*, driver=None) -> "UsageConfig":
        return UsageConfig(
            driver=driver,
            xplornet_username=os.environ["XPLORNET_USERNAME"],
            xplornet_password=os.environ["XPLORNET_PASSWORD"],
            email_server=os.environ["EMAIL_SERVER"],
            email_username=os.environ["EMAIL_USERNAME"],
            email_password=os.environ["EMAIL_PASSWORD"],
            email_sender=os.environ["EMAIL_SENDER"],
            email_recipients=[
                email.strip() for email in os.environ["EMAIL_RECIPIENTS"].split(",")
            ],
            debug=os.environ.get("DEBUG", "f").lower() in ["y", "yes", "true", "1"],
            debug_recipients=[
                email.strip()
                for email in os.environ.get(
                    "DEBUG_RECIPIENTS", os.environ["EMAIL_RECIPIENTS"]
                ).split(",")
            ],
        )
