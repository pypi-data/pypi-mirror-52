"""
the setup to install vault_printer
"""
import setuptools

from vault_printer import description, name, url, version

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name=name,
    version=version,
    author="Philip Molares",
    author_email="philipmolares@yahoo.de",
    description=description,
    entry_points={
        'console_scripts': [
            "vault_printer = vault_printer.main:main"
        ]
    },
    install_requires=["hvac", "hvac[parser]", "jinja2"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    url=url,
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
