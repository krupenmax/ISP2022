from setuptools import setup, find_packages


setup(
    name='serializer',
    version='1.0',
    packages=["serializer", "serializer/form", "factory"],
    scripts=['bin.py'],
    test_suite = 'test'
)