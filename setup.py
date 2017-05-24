from setuptools import setup


setup(
    name='openconnect_wrapper',
    version='0.2',
    py_modules=['openconnect_wrapper'],
    install_requires=[
        'Click==6.7',
        'psutil==5.2.2'
    ],
    entry_points='''
        [console_scripts]
        openconnect_wrapper=openconnect_wrapper:cli
    ''',
)
