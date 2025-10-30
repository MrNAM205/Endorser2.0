
import yaml

class ConfigManager:
    def __init__(self, config_path='config.yaml'):
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"ERROR: Config file not found at {config_path}")
            self.config = {}
        except Exception as e:
            print(f"ERROR: Failed to load or parse config file: {e}")
            self.config = {}

    def get(self, key, default=None):
        # Allows accessing nested keys using dot notation, e.g., "logging.log_level"
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

# Singleton instance
config_manager = ConfigManager()
