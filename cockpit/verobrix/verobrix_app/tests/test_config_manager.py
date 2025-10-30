import os
import pytest
from modules.config_manager import config

def test_system_name_is_loaded():
    """
    Tests that a basic value is correctly loaded from the config file.
    """
    assert config.get('system.name') == 'VeroBrix'

def test_get_output_path_is_absolute():
    """
    Tests that the get_output_path() method returns an absolute path.
    """
    output_path = config.get_output_path()
    assert os.path.isabs(output_path)

def test_get_output_path_ends_correctly():
    """
    Tests that the output path ends with the correct directory name.
    """
    output_path = config.get_output_path()
    # Use os.path.normpath to handle trailing slashes
    assert os.path.basename(os.path.normpath(output_path)) == 'output'

def test_log_level_is_uppercase():
    """
    Tests that the get_log_level() method returns an uppercase string.
    """
    assert config.get_log_level() == 'INFO'
