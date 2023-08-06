from setuptools import setup, find_packages
import datetime
import neptune_cache_redis

try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='neptune_cache_redis',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),  # Chose the same as "name",
    version=datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y.%m.%d.%H%M'),  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    long_description=long_description ,
    long_description_content_type='text/markdown',
    description='REDIS CACHE FOR NEPTUNE DNS SERVER',  # Give a short description about your library
    author='Yury (Yurzs)',  # Type in your name
    author_email='dev@best-service.online',  # Type in your E-Mail
    url='https://git.best-service.online/yurzs/neptune-cache-redis',  # Provide either the link to your github or to your website
    keywords=['NEPTUNE', 'CACHE', 'REDIS'],  # Keywords that define your package best
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
