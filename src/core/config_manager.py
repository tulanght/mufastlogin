# file-path: src/core/config_manager.py
# version: 2.0 (Final)
# last-updated: 2025-07-26
# description: Correctly handles a persistent settings.ini path for both development and the packaged .exe.

import configparser
from pathlib import Path
import sys
import os

class ConfigManager:
    """
    Manages reading and writing account configurations to an INI file.
    Ensures the settings.ini file is always located next to the executable.
    """
    def __init__(self, config_file: str = "settings.ini"):
        """
        Initializes the ConfigManager and determines the correct path for settings.ini.
        """
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (e.g., by PyInstaller)
            application_path = os.path.dirname(sys.executable)
        else:
            # If run in a normal Python environment
            application_path = Path(__file__).parent.parent.parent

        self.config_path = Path(application_path) / config_file
        self.config = configparser.ConfigParser()
        # Ensure the file exists on first run
        if not self.config_path.is_file():
            self._write_config()

    def _read_config(self):
        """Reads the configuration file into the parser."""
        self.config.read(self.config_path)

    def _write_config(self):
        """Writes the current configuration to the file."""
        with self.config_path.open('w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def get_all_accounts(self) -> list[str]:
        """
        Retrieves a list of all account names (sections) from the config file.
        """
        self._read_config()
        # Exclude the 'Coordinates' section from the account list
        accounts = [s for s in self.config.sections() if s != 'Coordinates']
        return accounts

    def get_password(self, account: str) -> str:
        """
        Retrieves the password for a specific account.
        """
        self._read_config()
        return self.config.get(account, 'password', fallback='')

    def save_account(self, account: str, password: str):
        """
        Saves or updates an account's password in the config file.
        """
        self._read_config()
        if not self.config.has_section(account):
            self.config.add_section(account)
        self.config.set(account, 'password', password)
        self._write_config()

    def delete_account(self, account: str) -> bool:
        """
        Deletes an account (section) from the config file.
        """
        self._read_config()
        if self.config.has_section(account) and account != 'Coordinates':
            self.config.remove_section(account)
            self._write_config()
            return True
        return False

    def save_coords(self, field_name, coords):
        """Saves coordinates for a specific field."""
        self._read_config()
        if not self.config.has_section('Coordinates'):
            self.config.add_section('Coordinates')
        self.config.set('Coordinates', field_name, f"{coords[0]},{coords[1]}")
        self._write_config()

    def load_coords(self):
        """Loads all coordinates from the [Coordinates] section."""
        self._read_config()
        coords = {}
        if not self.config.has_section('Coordinates'):
            return None
        try:
            if self.config.has_option('Coordinates', 'account'):
                acc_coords = self.config.get('Coordinates', 'account').split(',')
                coords['account'] = (int(acc_coords[0]), int(acc_coords[1]))
            if self.config.has_option('Coordinates', 'password'):
                pw_coords = self.config.get('Coordinates', 'password').split(',')
                coords['password'] = (int(pw_coords[0]), int(pw_coords[1]))
            return coords if coords else None
        except:
            return None