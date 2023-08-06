from setuptools import setup, find_packages

setup(
    name='neptune_cache_redis',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),  # Chose the same as 'name',
    version='2019.09.15.1347',
    # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    long_description='''# Neptune Resolver Rest
This module is made as a caching middleware for Neptune DNS server
## Installation
```pip3 install neptune_cache_redis```
## Connect to server
In config.py edit CACHE variable. Add ```'neptune_cache_redis'```  
It will look like this  
```CACHE = 'neptune_cache_redis'```  
Then you need to set settings for this cacher. Those settings are set by creating variable   in config.py with upper module name like this  
```NEPTUNE_CACHE_REDIS = {'host':'localhost', 'database': 1}```''',
    long_description_content_type='text/markdown',
    description='REDIS CACHE FOR NEPTUNE DNS SERVER',  # Give a short description about your library
    author='Yury (Yurzs)',  # Type in your name
    author_email='dev@best-service.online',  # Type in your E-Mail
    url='https://git.best-service.online/yurzs/neptune-cache-redis',
    # Provide either the link to your github or to your website
    keywords=['NEPTUNE', 'CACHE', 'REDIS'],  # Keywords that define your package best
    install_requires=['aioredis'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either '3 - Alpha', '4 - Beta' or '5 - Production/Stable' as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
