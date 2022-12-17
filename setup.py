from setuptools import setup, find_packages

setup(name='feasium',
    version='0.1',
    description='A simple static site generator',
    author='Austin Chang',
    author_email='austin880625@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Jinja2',
        'Markdown',
        'markdown-del-ins',
        'markdown-katex',
        'MarkupSafe',
        'pathlib2',
        'six'
    ],
    entry_points={'console_scripts': ['feasium=feasium.command_line:main']})