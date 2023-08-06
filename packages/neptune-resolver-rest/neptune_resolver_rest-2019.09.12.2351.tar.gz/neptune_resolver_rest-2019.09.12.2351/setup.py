from distutils.core import setup
import datetime

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='neptune_resolver_rest',  # How you named your package folder (MyLib)
    packages=['neptune_resolver_rest'],  # Chose the same as "name"
    version=datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y.%m.%d.%H%M'),  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='HTTP Request based resolver for NEPTUNE DNS SERVER',  # Give a short description about your library
    author='Yury (Yurzs)',  # Type in your name
    author_email='dev@best-service.online',  # Type in your E-Mail
    url='https://git.best-service.online/yurzs/neptune-resolver-rest',  # Provide either the link to your github or to your website
    keywords=['NEPTUNE', 'REST', 'RESOLVER'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'aiohttp',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
