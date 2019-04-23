import calendar
import datetime
import logging

from usage_monitor.config import UsageConfig
from usage_monitor.check import calculate_usage
from usage_monitor.send import send_alert, send_debug


def scan(config: UsageConfig):
    try:
        now = datetime.datetime.now()
        month_ratio = now.day / calendar.monthrange(now.year, now.month)[1]

        usage_ratio = calculate_usage(
            config.xplornet_username, config.xplornet_password
        )

        logging.info("Month: %f\nUsage: %f", month_ratio, usage_ratio)

        if usage_ratio > month_ratio:
            send_alert(
                config.email_server,
                config.email_username,
                config.email_password,
                config.email_sender,
                config.email_recipients,
                month_ratio,
                usage_ratio,
            )
    except Exception as e:
        logging.exception(e)
        if config.debug:
            send_debug(
                config.email_server,
                config.email_username,
                config.email_password,
                config.email_sender,
                config.debug_recipients,
                e,
            )


if __name__ == "__main__":
    config = UsageConfig.from_env()
    scan(config)
