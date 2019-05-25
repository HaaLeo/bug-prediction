# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

from os import path

from setuptools import find_packages, setup

# pylint: disable=exec-used,undefined-variable

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), 'r', encoding="utf8") as rf:
    LONG_DESCRIPTION = rf.read()

with open(path.join(path.abspath(path.dirname(__file__)), 'bugprediction/_version.py'), 'r', encoding="utf8") as f:
    exec(f.read())

setup(
    # PEP8: Packages should also have short, all-lowercase names, the use of underscores is discouraged
    name='bugprediction',
    version=__version__,
    packages=find_packages(exclude=['*test']),
    description='Predict bugs using the complexity of code changes.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/HaaLeo/bug-prediction',
    author='Leo Hanisch',
    license='BSD 3-Clause License',
    install_requires=[
        'gitpython>=2.1.1, <3.0.0'
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/HaaLeo/bug-prediction/issues',
        'Changelog': 'https://github.com/HaaLeo/bug-prediction/blob/master/CHANGELOG.md#changelog',
        'License': 'https://github.com/HaaLeo/bug-prediction/blob/master/LICENSE.txt'
    },
    python_requires='>=3.0',
    keywords=[
        'bug',
        'bugs',
        'bug-prediction',
        'bug-detection',
        'bugprediction',
        'fault',
        'fault-prediction',
        'faults',
        'fault-detection',
        'detection',
        'prediction',
        'entropy',
        'change',
        'complexity'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'Topic :: Scientific/Engineering'
    ],
    entry_points={
        'console_scripts': [
            'bugprediction=bugprediction.__main__:main'
        ]
    }
)
