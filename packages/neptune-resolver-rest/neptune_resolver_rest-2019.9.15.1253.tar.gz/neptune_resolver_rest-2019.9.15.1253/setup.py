from setuptools import setup, find_packages

setup(
    name='neptune_resolver_rest',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),  # Chose the same as "name"
    version='2019.09.15.1253',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    long_description='''# Neptune Resolver Rest
This module is made as a resolving middleware for Neptune DNS server
## Installation
```pip3 install neptune_resolver_rest```
## Connect to server
In config.py edit RESOLVERS variable. Add ```'neptune_resolver_rest'```
It will look like this
```RESOLVERS = ['neptune_resolver_rest']```
Then you need to set settings for this resolver. Those settings are set by creating variable in config.py with upper module name like
```NEPTUNE_RESOLVER_REST = {'base_url':'https://example.com'}```''',
    long_description_content_type='text/markdown',
    description='HTTP Request based resolver for NEPTUNE DNS SERVER',  # Give a short description about your library
    author='Yury (Yurzs)',  # Type in your name
    author_email='dev@best-service.online',  # Type in your E-Mail
    url='https://git.best-service.online/yurzs/neptune-resolver-rest',  # Provide either the link to your github or to your website
    keywords=['NEPTUNE', 'REST', 'RESOLVER'],  # Keywords that define your package best
    install_requires=['aiohttp'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
    ],
)