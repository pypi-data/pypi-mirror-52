from setuptools import setup, find_packages

SHORT_DESCRIPTION = 'CMake Analyzer (cmana) is a tool that helps developers to find common issues \
in CMake code. It searches for deprecated commands/keywords, bad codestyle, \
potential problems.'

LONG_DESCRIPTION = open('README.md', encoding='utf-8').read()

setup(
    name='cmake-analyzer',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'TatSu==4.4.0'
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'cmana=cmake_analyzer.analyzer:entrypoint',
        ],
    },

    url='https://bitbucket.org/ArchiDevil/cmake-analyzer',
    project_urls={
        'Homepage': 'https://bitbucket.org/ArchiDevil/cmake-analyzer',
        'Bug Tracker': 'https://bitbucket.org/ArchiDevil/cmake-analyzer/issues',
        'Source Code': 'https://bitbucket.org/ArchiDevil/cmake-analyzer/src',
    },

    author='Denis Bezykornov',
    author_email='archidevil52@gmail.com',
    keywords='cmake lint analyzer',
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    license='MIT'
)
