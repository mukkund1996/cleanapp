from setuptools import setup

with open("requirements.txt", "r") as reader:
    requirements = list(map(lambda s: s.rstrip("\n"), reader.readlines()))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cleanapp",
    version="1.0.0",
    description="The most compelling cleaning app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mukkund1996/cleanapp",
    author="Mukks",
    author_email="mukkundsunjii@gmail.com",
    license="MIT",
    packages=["cleanapp"],
    install_requires=requirements,
    zip_safe=False
)
