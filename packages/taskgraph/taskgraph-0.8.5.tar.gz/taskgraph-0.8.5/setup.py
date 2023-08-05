"""taskgraph setup.py."""
from setuptools import setup

LONG_DESCRIPTION = '%s\n\n%s' % (
    open('README.rst').read(),
    open('HISTORY.rst').read())

setup(
    name='taskgraph',
    use_scm_version={'version_scheme': 'post-release',
                     'local_scheme': 'node-and-date'},
    setup_requires=['setuptools_scm'],
    description='Parallel task graph framework.',
    long_description=LONG_DESCRIPTION,
    maintainer='Rich Sharp',
    maintainer_email='richpsharp@gmail.com',
    url='https://bitbucket.org/natcap/taskgraph',
    packages=['taskgraph'],
    license='BSD',
    keywords='parallel multiprocessing distributed computing',
    extras_require={
        'niced_processes': ['psutil'],
        },
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: System :: Distributed Computing',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: BSD License'
    ])
