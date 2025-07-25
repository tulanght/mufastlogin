# file-path: src/core/config_manager.py
# version: 1.0
# last-updated: 2025-07-25
# description: Handles all operations related to the settings.ini file,
#              including reading and writing account credentials. This module
#              is UI-independent.

import configparser
from pathlib import Path

class ConfigManager:
    """
    Manages reading and writing account configurations to an INI file.
    """
    def __init__(self, config_file: str = "settings.ini"):
        """
        Initializes the ConfigManager with the path to the config file.
        The file is placed in the project's root directory.
        """
        # Build the path to the root directory (up one level from src/)
        self.config_path = Path(__file__).parent.parent.parent / config_file
        self.config = configparser.ConfigParser()

    def _read_config(self):
        """Reads the configuration file into the parser."""
        self.config.read(self.config_path)

    def _write_config(self):
        """Writes the current configuration to the file."""
        with self.config_path.open('w') as configfile:
            self.config.write(configfile)

    def get_all_accounts(self) -> list[str]:
        """
        Retrieves a list of all account names (sections) from the config file.

        Returns:
            list[str]: A list of account names.
        """
        self._read_config()
        return self.config.sections()

    def get_password(self, account: str) -> str:
        """
        Retrieves the password for a specific account.

        Args:
            account (str): The name of the account (section).

        Returns:
            str: The password, or an empty string if not found.
        """
        self._read_config()
        return self.config.get(account, 'password', fallback='')

    def save_account(self, account: str, password: str):
        """
        Saves or updates an account's password in the config file.

        Args:
            account (str): The account name to be used as the section header.
            password (str): The password to save.
        """
        self._read_config()
        if not self.config.has_section(account):
            self.config.add_section(account)
        self.config.set(account, 'password', password)
        self._write_config()