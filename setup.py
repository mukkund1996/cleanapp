from setuptools import setup

with open("requirements.txt", 'r') as reader:
    requirements = list(map(lambda s: s.rstrip("\n"), reader.readlines()))

setup(
    name='cleanapp',
    version='1.0',
    description='The most compelling cleaning app',
    url='http://github.com/',
    author='Mukks',
    author_email='mukkundsunjii@gmail.com',
    license='MIT',
    packages=['cleanapp'],
    install_requires=requirements,
    zip_safe=False
)
