from usage_monitor.config import UsageConfig
from usage_monitor.scan import scan

if __name__ == "__main__":
    config = UsageConfig.from_env()
    scan(config)
