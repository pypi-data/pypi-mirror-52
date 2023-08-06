from setuptools import setup, find_packages

setup(
    name = "helloworldgeez",
    version="0.3.1",
    description="test pypl",
    packages=find_packages(),
    entry_points = {
        'console_scripts': ["helloworldgeez = helloworldgeez.cli:main"]
    }
)
