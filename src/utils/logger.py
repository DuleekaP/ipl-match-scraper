import logging
import logging.config
from pathlib import Path
from typing import Optional
import json
from config.settings import BASE_DIR

def setup_logging(
    default_path: Path = BASE_DIR / "config" / 'logging.conf',
    default_level: int = logging.INFO,
    env_key: str = "LOG_CFG"
) -> None:
    """Setup logging configuration"""
    path = default_path
    if path.exists():
        with open(path, "rt") as f:
            try:
                config = json.load(f)
                logging.config.dictConfig(config)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error in logging configuration file: {e}")
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print(f"Logging configuration file not found at {path}. Using default configuration.")

def get_logger(
        name: Optional[str] = None,
        log_file: Optional[Path] = None,
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
)-> logging.Logger:

    setup_logging()
    logger = logging.getLogger(name or 'root')
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_file:

        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setLevel(file_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

setup_logging()

