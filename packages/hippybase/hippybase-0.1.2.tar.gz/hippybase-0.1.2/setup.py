from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hippybase',
    version='0.1.2',
    description='A Python library to interact with Apache Hbase through its REST api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='WeiJi Hsiao',
    license='MIT License',
    packages=['hippybase'],
    install_requires=['requests', 'protobuf'],
    url='https://github.com/WeiJiHsiao/hippybase'
)
