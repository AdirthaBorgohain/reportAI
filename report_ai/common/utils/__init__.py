import os
from box import Box
from pathlib import Path
from dotenv import load_dotenv
from report_ai.common.utils.logger import Logger
from report_ai.common.utils.helpers import load_yaml_file

root_dir = Path(__file__).parent.absolute().parent.parent
base_dir = os.path.join(root_dir, "common")
print("root_dir: ", root_dir)

log_dir = os.path.join(root_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

assets_dir = os.path.join(root_dir, "assets")
os.makedirs(log_dir, exist_ok=True)

reports_dir = os.path.join(root_dir, "reports")
os.makedirs(reports_dir, exist_ok=True)

load_dotenv()

# Load configuration files
config_path = os.getenv("config_path",
                        default=os.path.join(base_dir, "utils/configs.yaml"))
configs = load_yaml_file(config_path)

logger_handler = Logger(log_file_name="report-ai.log", log_path=log_dir)
logger = logger_handler.create_time_rotating_log(when="day", backup_count=10, name="report-ai")

# Update configs
configs["root_dir"] = root_dir
configs["assets_dir"] = assets_dir
configs["reports_dir"] = reports_dir
configs["logger"] = logger

# configs = Box(configs)

__all__ = ['configs']
