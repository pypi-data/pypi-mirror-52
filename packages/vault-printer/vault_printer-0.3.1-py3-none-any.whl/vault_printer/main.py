#!/bin/env python3
"""
this script gets all entries of a kv store on a vault server
and puts it in txt file for easy paper storage
"""

from __future__ import annotations

import os
from argparse import ArgumentParser
import logging as log
from typing import List

from hvac import Client

from vault_printer import description, name, url, version
from vault_printer.entities import Entity, Folder, Object
from vault_printer.config import Config


def get_base_folder(client: Client, kv_store: str) -> Folder:
    """
    get the base folder
    :param client: the client to connect with
    :param kv_store: the kv_store from which to retrieve the folder
    :return: a folder object
    """
    log.info("getting secrets for %s", kv_store)
    if not kv_store.endswith("/"):
        kv_store = kv_store + "/"
    folder: Folder = Folder(kv_store)
    folder.content = get_folder_content(client, "", kv_store)
    return folder


def get_folder_content(client: Client, path: str, mount_point: str) -> List[Object]:
    """
    get the list of content for a base folder
    :param client: the client to connect with
    :param path: the path in the kv_store to the entity in question
    :param mount_point:  the kv_store from which to retrieve the objects
    :return: a list of either folders or entities
    """
    keys: List[str] = []
    content: List[Object] = []
    try:
        keys = client.secrets.kv.v2.list_secrets(
            path=path,
            mount_point=mount_point
        )['data']['keys']
    except ValueError as err:
        log.error("Error: %s", err)
    log.info("found a folder " + mount_point + path)
    for key in keys:
        if key.endswith('/'):
            # this seems to be a folder
            folder = Folder(key)
            folder.content = get_folder_content(client, path + key, mount_point)
            content.append(folder)
        else:
            # this seems to be an entity
            content.append(get_entity(client, path, key, mount_point))
    return content


def get_entity(client: Client, path: str, entity_name: str, mount_point: str) -> Entity:
    """
    get an entity object from  the api
    :param client: the client to connect with
    :param path: the path in the kv_store to the entity in question
    :param entity_name: the name (for easy inserting in the entity object)
    :param mount_point: the kv_store from which to retrieve the entity
    :return: an entity object
    """
    data = {}
    try:
        data = client.secrets.kv.v2.read_secret_version(
            path=path + "/" + entity_name,
            mount_point=mount_point
        )['data']
    except ValueError as err:
        log.error("Error: %s", err)
    log.info("found an entity %s with ", str(data['data'].keys()))
    return Entity(entity_name, data)


def main() -> None:
    """
    the main function loop
    :return: None
    """
    parser = ArgumentParser(description=description)
    parser.add_argument('--version',
                        action='version',
                        version=version)
    parser.add_argument('-v', "--verbose",
                        help='increase verbosity',
                        action='store_true',
                        default=False)

    server_group = parser.add_argument_group(title='server parameter')
    server_group.add_argument('url',
                              help='the url of the vault server',
                              type=str,
                              nargs='?',
                              default=os.environ.get('VAULT_ADDR', ''))
    server_group.add_argument('kv_store',
                              help='the kv store to export from',
                              type=str)

    output_group = parser.add_argument_group(title="output configuration")
    output_group.add_argument('--no-toc',
                              help='don\'t print the toc',
                              action='store_true',
                              default=False)
    output_group.add_argument('--no-content',
                              help='don\'t print the content',
                              action='store_true',
                              default=False)

    # login method group
    login_group = parser.add_mutually_exclusive_group(required=False)
    login_group.add_argument('--ldap',
                             help='login via ldap',
                             action='store_true')
    login_group.add_argument('--token',
                             help='login via token',
                             action='store_true')

    login_parameter_group = parser.add_argument_group(title='login parameter')
    login_parameter_group.add_argument('--username', '-u',
                                       help="the username with which to login, "
                                       + "if omitted you\'ll be asked")
    login_parameter_group.add_argument('--password', '-p',
                                       help='the password to login, if omitted you\'ll be asked')
    login_parameter_group.add_argument('--tokenLogin', '-t',
                                       help='the  token to login, if omitted you\'ll be asked',
                                       default=os.environ.get('VAULT_TOKEN', ''))

    args = parser.parse_intermixed_args()

    if args.verbose:
        log.basicConfig(format="%(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(message)s")

    if args.no_toc and args.no_content:
        log.error("the usage of --no-toc and --no-content together does not produce any output")
        log.error("Aborting...")
        exit(2)

    config: Config = Config(args.url, args.kv_store)

    if args.ldap:
        client = config.login_via_ldap(args.username, args.password)
    elif args.token:
        client = config.login_via_token(args.tokenLogin)
    else:
        client = config.login()

    config.log()

    folder: Folder = get_base_folder(client, config.kv_store)

    print("`created by {name} {version} ({url})`\n".format(name=name, version=version, url=url))

    if not args.no_toc:
        print(folder.toc())

    if not args.no_content:
        print(folder.print())


if __name__ == "__main__":
    main()
