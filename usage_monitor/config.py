import configparser
import os
import typing


class UsageConfig(typing.NamedTuple):
    xplornet_username: str
    xplornet_password: str

    email_server: str
    email_username: str
    email_password: str
    email_sender: str
    email_recipients: typing.List[str]

    @staticmethod
    def from_file(filename: str) -> "UsageConfig":
        config = configparser.ConfigParser()
        config.read(filename)

        return UsageConfig(
            xplornet_username=config["xplornet"]["username"],
            xplornet_password=config["xplornet"]["password"],
            email_server=config["email"]["server"],
            email_username=config["email"]["username"],
            email_password=config["email"]["password"],
            email_sender=config["email"]["sender"],
            email_recipients=[
                email.strip() for email in config["email"]["recipients"].split(",")
            ],
        )

    @staticmethod
    def from_env() -> "UsageConfig":
        return UsageConfig(
            xplornet_username=os.environ["XPLORNET_USERNAME"],
            xplornet_password=os.environ["XPLORNET_PASSWORD"],
            email_server=os.environ["EMAIL_SERVER"],
            email_username=os.environ["EMAIL_USERNAME"],
            email_password=os.environ["EMAIL_PASSWORD"],
            email_sender=os.environ["EMAIL_SENDER"],
            email_recipients=[
                email.strip() for email in os.environ["EMAIL_RECIPIENTS"].split(",")
            ],
        )
