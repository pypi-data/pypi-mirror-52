# -*- coding: utf-8 -*-
"""Installer for the collective.denyroles package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [open("README.rst").read(), open("CONTRIBUTORS.rst").read(), open("CHANGES.rst").read()]
)


setup(
    name="collective.denyroles",
    version="1.0.0b2",
    description="Plone PAS patch for denying access to editors and managers",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Maurits van Rees",
    author_email="m.van.rees@zestsoftware.nl",
    url="https://github.com/collective/collective.denyroles/",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=["setuptools"],
    extras_require={"test": ["plone.app.testing"]},
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
