"""
Test Main
"""

import argparse
import os
import unittest
from unittest import mock

from vault_printer.main import main


class MainTest(unittest.TestCase):
    """
    Test Cases
    """

    @mock.patch('argparse.ArgumentParser.parse_intermixed_args',
                return_value=argparse.Namespace(verbose=False,
                                                url=os.environ.get("VAULT_ADDR", None),
                                                kv_store="admin",
                                                ldap=True, token=False,
                                                username=os.environ.get("VAULT_USER", None),
                                                password=os.environ.get("VAULT_PASS", None),
                                                no_toc=True,
                                                no_content=True))
    def test_no_url_exit(self, _mock_args):
        """
        check that a url is needed
        :param mock_args: a mocking of argparse parameters
        :return: None
        """
        with self.assertRaises(SystemExit):
            main()


if __name__ == '__main__':
    unittest.main()
