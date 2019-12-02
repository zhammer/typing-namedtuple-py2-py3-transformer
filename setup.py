from setuptools import find_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="typing-namedtuple-transformer",
    version="0.1.6",
    description="libcst codemod for updating typing.NamedTuple py2 backport to native py3 syntax",
    url="https://github.com/zhammer/typing-namedtuple-transformer",
    packages=find_packages(exclude=["tests", "demo_site"]),
    package_data={"typing_namedtuple_transformer": ["py.typed"]},
    install_requires=["libcst >= 0.2.4"],
    author="Zach Hammer",
    author_email="zachary_hammer@alumni.brown.edu",
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
