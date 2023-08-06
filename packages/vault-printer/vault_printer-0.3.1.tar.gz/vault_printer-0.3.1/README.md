# vault_printer ![pylint 10.00][pylint-badge] [![MIT License][license-badge]](LICENSE.md) [![PyPI version][pypi-badge]][pypi-project] [![python version][pypi-python]][pypi-project]
vault_printer is a little program to extract a whole kv_store of a [Vault Server][vaultproject] to stdout in markdown.
This could be used to print it out and store it in a physical safe somewhere. Or at least that's the purpose for which I wrote it.

## Install

Get a stable version from [PyPi][pypi]

`pip install vault_printer`

or via git

`pip install git+https://github.com/DerMolly/vault_printer`

## Usage

E.g extract kv_store `test` from `vault.example.com` and login via ldap:

`vault_printer --ldap vault.example.com test >> passwords.md `

### Help

```
usage: vault_printer [-h] [--version] [-v] [--no-toc] [--no-content]
                     [--ldap | --token] [--username USERNAME]
                     [--password PASSWORD] [--tokenLogin TOKENLOGIN]
                     [url] kv_store

A program to get all secrets from a vault servers kv_store for printing

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         increase verbosity
  --ldap                login via ldap
  --token               login via token

server parameter:
  url                   the url of the vault server
  kv_store              the kv store to export from

output configuration:
  --no-toc              don't print the toc
  --no-content          don't print the content

login parameter:
  --username USERNAME, -u USERNAME
                        the username with which to login, if omitted you'll be
                        asked
  --password PASSWORD, -p PASSWORD
                        the password to login, if omitted you'll be asked
  --tokenLogin TOKENLOGIN, -t TOKENLOGIN
                        the token to login, if omitted you'll be asked
```


### Login

Currently the only supported login methods are:

- Token
- LDAP

Maybe I will add some more in the future. If you need another Login Method feel free to open a [issue][tracker] or even a PR.

### Environment Variables

This program also uses these environment variables if set

`$VAULT_ADDR`  : the url of the vault server  
`$VAULT_TOKEN` : the token to authenticate with the `--token` login method 


[pylint-badge]:   https://mperlet.github.io/pybadge/badges/10.00.svg
[license-badge]:  https://img.shields.io/badge/license-MIT-007EC7.svg
[pypi-badge]:     https://badge.fury.io/py/vault-printer.svg
[pypi-project]:   https://pypi.org/project/vault_printer/
[pypi-python]:    https://img.shields.io/pypi/pyversions/vault-printer
[vaultproject]:   https://www.vaultproject.io/
[pypi]:           https://pypi.org/
[tracker]:        https://github.com/DerMolly/vault_printer/issues