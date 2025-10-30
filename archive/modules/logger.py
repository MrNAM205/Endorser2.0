
import logging
import os
from modules.config_manager import config_manager

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # Also log to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handler)

    return logger

# --- System Logger ---
log_level_str = config_manager.get("logging.log_level", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)

system_log_file = config_manager.get("logging.system_log_file", "logs/system.log")
system_logger = setup_logger('SystemLogger', system_log_file, log_level)

# --- Provenance Logger ---
# This logger is for tracking the agent's actions and decisions, as per the project vision.
provenance_log_file = config_manager.get("logging.provenance_log_file", "logs/provenance.log")
provenance_logger = setup_logger('ProvenanceLogger', provenance_log_file, logging.INFO)

def log_provenance(agent_name, action, details):
    provenance_logger.info(f"AGENT={agent_name}, ACTION={action}, DETAILS=[{details}]")
