import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccpl",
    version="0.2.0",
    author="Rainbow Doge",
    author_email="realrainbowdoge@gmail.com",
    description="ColorfulCore Python Library - CCPL for short.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.jakubwilk.me",
    packages=setuptools.find_packages(),
    install_requires = ['pytube','bs4','requests','os'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)