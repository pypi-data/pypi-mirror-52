from setuptools import setup, find_packages

version = '1.2.1'

setup(
    name='lucy',
    version=version,
    description='CLI to create a LICENSE file',
    long_description='Lucy generates a LICENSE file for your project from the command line for you.',
    author='Chinmaya Kr. Patanaik',
    author_email='patanaikchinmaya@gmail.com',
    license='MIT',
    keywords=['license', 'github', 'command line', 'cli'],
    url='https://github.com/pattu777/Lucy',
    packages=find_packages(),
    install_requires=[
        'Click',
	'requests',
    ],
    entry_points={
        'console_scripts': [
            'lucy=lucy.lucy:main'
        ],
    }
)
