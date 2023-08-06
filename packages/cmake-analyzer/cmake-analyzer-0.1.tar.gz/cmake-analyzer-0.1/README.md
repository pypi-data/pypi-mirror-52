# CMake Analyzer

CMake Analyzer (`cmana`) is a tool that helps developers to find common issues
in CMake code. It searches for deprecated commands/keywords, bad codestyle,
potential problems.

## Installation

    $ pip install cmake-analyzer

## Usage
This tool works by both `python -m cmake_analyzer` and `cmana` console commands.

Simple usage pattern:

    $ cmana -p /some/directory/to/your/project

Full help is available by `-h` key as the following:

    $ cmana -h
    usage: cmana [-h] [-c CHECKS [CHECKS ...]] [-v] [--custom-checks PATH]
                (-p PATH | --list-checks) [--exclude EXCLUDE [EXCLUDE ...] |
                --include INCLUDE [INCLUDE ...]]

    optional arguments:
        -h, --help            show this help message and exit
        -c CHECKS [CHECKS ...], --checks CHECKS [CHECKS ...]
                                enable checks in the following format: style* legacy*
        -v, --verbose         enable verbose logging for large projects
        --custom-checks PATH  directory with user-defined checks
        -p PATH, --path PATH  path to start check from
        --list-checks         list all available checks
        --exclude EXCLUDE [EXCLUDE ...]
                                filter out files by mask
        --include INCLUDE [INCLUDE ...]
                                include only files by mask

## License

You may use CMake Analyzer under the terms of the MIT license
described in the enclosed `LICENSE.md` file.
