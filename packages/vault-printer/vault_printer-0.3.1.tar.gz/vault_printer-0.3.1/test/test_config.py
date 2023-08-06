"""
Test Config
"""

import os
from pathlib import Path
import unittest
from unittest.mock import patch

from vault_printer.config import Config, Method

VAULT_TOKEN: Path = Path(os.path.expanduser("~") + "/.vault_token")
VAULT_TOKEN_BAK: Path = Path(os.path.expanduser("~") + "/.vault_token.bak")


def move_vault_token_out_of_the_way() -> None:
    """
    move the .vault_token out of the way
    :return: None
    """
    if VAULT_TOKEN.is_file():
        os.rename(str(VAULT_TOKEN), str(VAULT_TOKEN_BAK))


def move_vault_token_back() -> None:
    """
    move the .vault_token.bak back
    :return: None
    """
    if VAULT_TOKEN_BAK.is_file():
        os.rename(str(VAULT_TOKEN_BAK), str(VAULT_TOKEN))


class ConfigTest(unittest.TestCase):
    """
    ConfigTest class
    """

    def test_config_no_url(self) -> None:
        """
        test that a config with no url raises an exception
        :return: None
        """
        with self.assertRaises(SystemExit):
            Config("", "")

    def test_config_no_kv_store(self) -> None:
        """
        test what a config looks like without a kv_store
        """
        move_vault_token_out_of_the_way()
        config: Config = Config(os.environ.get("VAULT_ADDR", None), "admin")
        self.assertEqual(config.url, os.environ.get("VAULT_ADDR", None))
        self.assertFalse(config.authenticated)
        self.assertEqual(config.username, "")
        self.assertEqual(config.password, "")
        self.assertEqual(config.token, "")
        self.assertEqual(config.method, Method.NotNeeded)
        move_vault_token_back()

    def test_config_vault_token(self) -> None:
        """
        check that a config with a present .vault_token is authenticated
        :return: None
        """
        move_vault_token_out_of_the_way()
        with open(str(VAULT_TOKEN), "a+") as file:
            file.write("test")
        config: Config = Config(os.environ.get("VAULT_ADDR", None), "admin")
        self.assertTrue(config.authenticated)
        os.remove(str(VAULT_TOKEN))
        move_vault_token_back()

    @patch('builtins.input', lambda *args: os.environ.get("VAULT_USER", None))
    def test_ask_for_username(self) -> None:
        """
        test if asking for a username works.
        using @patch to mock input
        :return: None
        """
        config: Config = Config(os.environ.get("VAULT_ADDR", None), "admin")
        config.ask_for_username()
        self.assertEqual(config.username, os.environ.get("VAULT_USER", None))


if __name__ == '__main__':
    unittest.main()
