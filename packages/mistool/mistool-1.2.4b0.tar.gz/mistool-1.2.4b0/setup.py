# ------------------------------------------------ #
# -- LINE COMMANDS FOR TWINE (which uses HTTPS) -- #
# ------------------------------------------------ #

# Source: https://pypi.python.org/pypi/twine

#     1) Create some distributions in the normal way:
#         > python setup.py sdist bdist_wheel
#
#     2) Upload with twine:
#         > twine upload dist/* --skip-existing


# -------------------- #
# -- STANDARD TOOLS -- #
# -------------------- #


# MAJ Z + pandoc pas sur 3.7 !!!

from setuptools import setup, find_packages
from pathlib import Path

# import pypandoc

# ----------------- #
# -- README FILE -- #
# ----------------- #

READ_ME_FILE = Path(__file__).parent / 'README.md'

with READ_ME_FILE.open(
    mode     = "r",
    encoding = "utf-8"
) as file:
    longdesc = file.read()


# ----------------- #
# -- OUR SETTNGS -- #
# ----------------- #

setup(
# General
    name         = "mistool",
    version      = "1.2.4-beta",
    url          = 'https://github.com/bc-python/mistool',
    license      = 'GPLv3',
    author       = "Christophe BAL",
    author_email = "projetmbc@gmail.com",

# Descritions
    long_description              = longdesc,
    long_description_content_type = "text/markdown",
    description                   = "Miscellaneous missing tools that can help the py-developper.",

# What to add ?
    packages = find_packages(),

# Uggly classifiers
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Desktop Environment :: File Managers',
        'Topic :: System :: Logging',
        'Topic :: Text Processing :: Markup :: LaTeX'
    ],

# What does your project relate to?
    keywords = 'python latex os path string terminal tool',
)
