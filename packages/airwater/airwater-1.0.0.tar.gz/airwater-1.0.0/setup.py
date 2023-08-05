# -*- coding: utf-8 -*-
import io

from setuptools import setup

with io.open("README.rst", "r", encoding="utf-8") as f:
    readme = f.read()

about = {}
with io.open("airwater/_version.py", "r", encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="airwater",
    version=about["__version__"],
    description="Better Tools Library For Write Spider With Python",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://airwater.readthedocs.io",
    author="Airwater",
    author_email="airwater@gmail.com",
    license="Apache 2.0",
    packages=["airwater"],
    zip_safe=False,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=[
        "python-dateutil",
        "arrow>=0.14.6"
        # "backports.functools_lru_cache>=1.2.1;python_version=='2.7'",
    ],
    test_suite="tests",
    tests_require=["chai", "mock"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="airwater spider library tools",
    project_urls={
        "Repository": "https://github.com/airwa/airwater",
        "Bug Reports": "https://github.com/airwa/airwater/issues",
        "Documentation": "https://airwater.readthedocs.io",
    },
)