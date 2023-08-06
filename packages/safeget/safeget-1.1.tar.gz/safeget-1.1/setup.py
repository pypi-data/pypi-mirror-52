'''
    Set up for safeget

    Copyright 2018-2019 DeNova
    Last modified: 2019-09-22
'''
import os
import setuptools

# read long description
with open("DESCRIPTION.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="safeget",
    version="1.1",
    author="denova.com",
    author_email="support@denova.com",
    maintainer="denova.com",
    maintainer_email="support@denova.com",
    description="Safeget gets and verifies files. It does the security checks that almost everyone skips.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="download,verification,sigs",
    license="GNU General Public License v3 (GPLv3)",
    url="https://denova.com/safeget/",
    download_url="https://github.com/denova/safeget/",
    project_urls={
        "Documentation": "https://denova.com/safeget/",
        "Source Code": "https://github.com/denova/safeget/",
    },
    include_package_data=False,
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
         ),
    entry_points={
        'console_scripts': [
            'safeget = safeget.safeget:main',
        ],
    },
    setup_requires=['setuptools-markdown'],
    install_requires="",
    requires="",
)
