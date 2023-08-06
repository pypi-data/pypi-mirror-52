"""
holds the folder and entities which represent the kv_store in vault
"""

from typing import List, Dict

from jinja2 import Template

TEMPLATE: Template = Template(u"""#### {{header}}
{% for key, value in dict.items() %}
{{"  - %s" | format(key)}}
{{"    - %s" | format(value)}}{% endfor %}\n\n\n""")


class Object:  # pylint: disable=too-few-public-methods
    """
    super class representing a Folder or a Entity
    """

    def toc_rec(self, indent: str, child: bool) -> str:
        """
        recursive function to build the table of contents
        :param indent: the indentation string
        :param child: if the object is the last child
        :return: the table of contents
        """

    def output(self, path: str, template: Template) -> str:
        """
        recursive function to generate a complete list of all entries with template
        :param path: the path of the object so far
        :param template: the template to format the output
        :return: the list of all entries in the kv store
        """


class Folder(Object):
    """
    representing a folder in the kv-store secret engine
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.content: List[Object] = []

    def append(self, obj: Object) -> None:
        """
        append obj to the content list
        :param obj: the object to add
        :return: None
        """
        self.content.append(obj)

    def toc(self) -> str:
        """
        start function for the recursive generation of the table of contents
        :return: the table of contents
        """
        output = "### Table of Contents\n\n```\n"
        output = output + "{}\n".format(self.name)
        for i, obj in enumerate(self.content):
            output += obj.toc_rec("  ", i is len(self.content)-1)
        output = output + "```\n"
        return output

    def toc_rec(self, indent: str, child: bool) -> str:
        output = indent
        if child:
            output += "  └── "
            indent += "  "
        else:
            output += "  ├── "
            indent += "  │  "
        output += self.name + "\n"

        for i, obj in enumerate(self.content):
            output += obj.toc_rec(indent, i is len(self.content)-1)

        return output

    def print(self) -> str:
        """
        start function for the recursive generation of the list of all entries in the kv store
        :return: the list of all entries in the kv store
        """
        output = "### Content of '{}'\n\n".format(self.name)
        output += self.output("", TEMPLATE)
        return output

    def output(self, path: str, template: Template) -> str:
        output = ""
        for obj in self.content:
            output += obj.output(path+self.name, template)
        return output


class Entity(Object):
    """
    representing an collection of key-value-pairs in the kv-store secret engine
    """

    def __init__(self, name: str, content: Dict[str, str]):
        self.name: str = name
        self.content: Dict[str, str] = content

    def toc_rec(self, indent: str, child: bool) -> str:
        output = indent
        if child:
            output += "  └── "
        else:
            output += "  ├── "
        output += self.name + "\n"
        return output

    def output(self, path: str, template: Template) -> str:
        return template.render(header=path+self.name, dict=self.content['data'])
