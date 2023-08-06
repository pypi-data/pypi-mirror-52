import io
import re
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("mznb/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)


setup(
    name="mznb-pdenno",
    version=version,
    url="https://github.com/pdenno/mznb/",
    project_urls={
        "Documentation": "https://github.com/pdenno/mznb/",
        "Code": "https://github.com/pdenno/mznb/",
        "Issue tracker": "https://github.com/pdenno/mznb/issues",
    },
    license="BSD",
    author="Peter Denno",
    author_email="podenno@gmail.com",
    maintainer="Peter Denno",
    maintainer_email="podenno@gmail.com",
    description="Magic to communicate between Jupyter notebooks and MiniZinc nb-agent",
    long_description=readme,
    packages=["mznb"],
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
    

