# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='zomato-top-ten',
    version = '1.0.0',
    description= 'top 10 restaurants in a category in a city',
    author = 'yvvarun',
    author_email = 'yvvarun@gmail.com',
    url = 'https://github.com/yvvarun/zomato-top-ten',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'zomato_top_ten = zomato_top_ten.zomato_top_ten:main',
        ]
    },
    install_requires=[
        'prettytable',
    ],
)
