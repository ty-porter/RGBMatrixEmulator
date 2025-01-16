import json, logging

# Try to load the config from file. (Default: INFO)
try:
    with open("emulator_config.json") as config_file:
        log_level_name = json.load(config_file).get("log_level", "INFO").upper()
        log_level = getattr(logging, log_level_name)
except:
    log_level = logging.INFO

# Create a Logger
Logger = logging.getLogger("RGBME")
Logger.setLevel(log_level)

# Create console handler and set the log level
ch = logging.StreamHandler()
ch.setLevel(log_level)

# Create formatter
formatter = logging.Formatter(
    "[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Add formatter to console handler
ch.setFormatter(formatter)

# Add console handler to Logger
Logger.addHandler(ch)
