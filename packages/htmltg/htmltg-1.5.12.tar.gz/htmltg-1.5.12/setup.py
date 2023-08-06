from setuptools import setup, find_packages

setup(
    name='htmltg',
    version='1.5.12',
    author='Elena Vysotskaya',
    url="https://github.com/alenavysotskaya4324/tagcounter",
    packages=find_packages(),
    description='app for counting tag of site page',
    package_data={'': ['*.db', '*.yaml', '*.pickle']},
    entry_points={'console_scripts': ['htmltg = tagcounter.console:main']},
)
