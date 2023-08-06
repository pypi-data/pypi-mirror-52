import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

homepath = os.path.expanduser('~')

setuptools.setup(
    name="lg-shell",
    version="0.0.0a3",
    author="Lionel Gulich",
    author_email="lgulich@ethz.ch",
    url="https://github.com/lgulich/lgshell",
    description="A command line utility for systems setup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/lgulich/lg-shell/archive/v0.0.alpha3.tar.gz",

    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
    ],
    license="GPL-3.0",


    package_dir={'': 'lib'},
    packages=setuptools.find_packages('lib'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'lgs = lg_shell:main.main',
        ]
    },
    data_files=[('/' + homepath + '/.config/lg_shell', ['lib/lg_shell/cfg/config.json'])],
    python_requires=">=3.5",
)
