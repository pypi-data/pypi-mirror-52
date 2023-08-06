'''
:author: Leandro (Cerberus1746) Benedet Garcia
'''
import os
import sys
import re

import setuptools

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR, "src"))

try:
    #pylint: disable=import-error
    from sphinx.setup_command import BuildDoc  # @UnresolvedImport
    SPHINX_LOADED = True
except ImportError:
    SPHINX_LOADED = False

NAME = 'panda_core_data'


def open_file(file_name):
    with open(file_name, "r") as file_handle:
        return file_handle.read()


def stripped_file(file_name):
    return open_file(file_name).strip().split("\n")


def find_version():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    version_file = open_file(os.path.join(current_dir, "src", NAME, "__version__.py"))
    version_match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", version_file)
    if version_match:
        return version_match.group(1)


if SPHINX_LOADED:
    CMDCLASS = {'build_sphinx': BuildDoc}

__version__ = find_version()


LONG_DESCRIPTION = open_file("README.md")
LICENSE = open_file("LICENSE")

REQUIREMENTS = stripped_file("requirements.txt")
TEST_PACKAGES = stripped_file("requirements-tests.txt")
REQUIREMENTS_DOCS = stripped_file("requirements-docs.txt")

setuptools.setup(
    name=NAME,
    version=__version__,
    cmdclass=CMDCLASS if SPHINX_LOADED else {},
    author="Leandro (Cerberus1746) Benedet Garcia",
    author_email="leandro.benedet.garcia@gmail.com",
    description="Data management system using plain text files like json and yaml.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT License",
    python_requires=">=3.7",
    url="https://github.com/Cerberus1746/PandaCoreData",
    tests_require=["pytest-runner"],
    packages=["src/" + NAME,],
    setup_requires=REQUIREMENTS,
    extras_require={
        'tests': TEST_PACKAGES,
        'docs': REQUIREMENTS_DOCS
    },
    install_requires=REQUIREMENTS,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

        "Development Status :: 2 - Pre-Alpha",

        "Intended Audience :: Developers",

        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', NAME),
            'version': ('setup.py', __version__),
            'source_dir': ('setup.py', 'docs/source'),
            'build_dir': ('setup.py', 'docs/build'),
        }
    } if SPHINX_LOADED else {},
)
