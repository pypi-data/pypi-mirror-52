"""
the config which holds the login information and the execution parameters
"""
import logging as log
import os
from enum import Enum
from getpass import GetPassWarning, getpass
from pathlib import Path

from hvac import Client
from hvac.exceptions import InvalidPath


class Method(Enum):
    """
    enum to represent login methods
    """
    NotNeeded = 1
    Token = 2
    LDAP = 3


class Config:
    """
    holds the config for this tool
    """

    def __init__(self, url: str, kv_store: str):
        self.kv_store = kv_store
        if not url.strip():
            log.error("No url provided")
            log.error("you can either specify this via $VAULT_ADDR "
                      "or as the first parameter to this program")
            log.error("Aborting...")
            exit(2)
        else:
            self.url = url.strip()
        vault_token: Path = Path(os.path.expanduser("~") + "/.vault_token")
        if vault_token.is_file():
            log.info("found ~/.vault-token")
            self.authenticated = True
        else:
            self.authenticated = False
        self.username = ""
        self.password = ""
        self.token = ""
        self.method = Method.NotNeeded

    @staticmethod
    def ask_for_secret(question: str) -> str:
        """
        ask for a secret.
        the input isn't shown on the terminal
        :param question: the secret that is asked (e.g. 'token' or 'password')
        :return: the user input
        """
        print("You did not provide " + question + ". Please enter it now")
        try:
            secret = getpass(prompt=question.capitalize() + ": ")
        except GetPassWarning as err:
            log.error('ERROR: %s', err)
        else:
            return secret

    def ask_for_password(self) -> None:
        """
        alias for ask_for_secret("password")
        """
        log.info("asking for password")
        self.password = self.ask_for_secret("password")

    def ask_for_token(self) -> None:
        """
        alias for ask_for_secret("token")
        """
        log.info("asking for token")
        self.token = self.ask_for_secret("token")

    def ask_for_username(self) -> None:
        """
        ask the user for a username
        """
        log.info("asking for username")
        while self.username is None or not self.username:
            print("You did not provide a username. Please enter it now")
            self.username = input("Username: ")

    def login_via_ldap(self, username: str, password: str) -> Client:
        """
        trying to login via ldap with username and password
        :param username: the username to login with
        :param password: the password to login with
        :return: the logged in client
        """
        if not self.authenticated:
            self.method = Method.LDAP
            if username and username.strip():
                self.username = username
            else:
                self.ask_for_username()
            if password and password.strip():
                self.password = password
            else:
                self.ask_for_password()

        return self.login()

    def login_via_token(self, token: str) -> Client:
        """
        trying to login via token
        :param token: the token to login with
        :return: the logged in client
        """
        if not self.authenticated:
            self.method = Method.Token
            if token:
                log.info("setting token")
                self.token = token
            else:
                self.ask_for_token()

        return self.login()

    def log(self) -> None:
        """
        write a log with the given config
        :return: None
        """
        log.info("got the following arguments:")
        log.info("  url:      %s", self.url)
        log.info("  kv_store: %s", self.kv_store)
        log.info("  method:   %s", self.method.__str__())
        if self.method is Method.LDAP:
            log.info("  username: %s", self.username)
            log.info("  password: <redacted>")
        if self.method is Method.Token:
            log.info("  token:    <redacted>")

    def login(self) -> Client:
        """
        create a client and log it in with the correct method
        :return: a logged in client
        """
        client = Client(self.url)
        log.info("client created with url %s", client.url)

        if not client.is_authenticated():
            log.info("client is not authenticated")

            if self.method == Method.LDAP:
                log.info("trying to login with LDAP")
                try:
                    client.auth.ldap.login(self.username, self.password)
                except (InvalidPath, ValueError) as err:
                    log.error("LDAP Login failed: %s", err)
                    exit(2)

            if self.method == Method.Token:
                log.info("trying to login with Token")
                try:
                    client.token = self.token
                    client.login(self.url, True)
                except (InvalidPath, ValueError) as err:
                    log.error("Token Login failed: %s", err)
                    exit(2)

        if not client.is_authenticated():
            log.error("login failed.")
            log.error("Aborting...")
            exit(2)

        return client
