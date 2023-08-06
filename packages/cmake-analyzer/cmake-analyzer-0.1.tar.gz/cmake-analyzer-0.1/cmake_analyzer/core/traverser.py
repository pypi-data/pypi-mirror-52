from enum import Enum
import os
import re
import fnmatch

from .parser import CMakeParser
from .reporter_base import create_full_diagnostic
from ..reporters import simple


class Mode(Enum):
    GLOBAL = 0


class Traverser:
    def __init__(self,
                 parser: CMakeParser,
                 checkers=[],
                 reporters=[simple.SimpleReporter()],
                 include_filters=None,
                 exclude_filters=None,
                 mode=Mode.GLOBAL,
                 verbose=False):
        if not parser or not isinstance(parser, CMakeParser):
            raise TypeError('parser argument must be of type CMakeParser()')

        if include_filters and exclude_filters:
            raise ValueError(
                'include_filters and exclude_filters cannot be set at the same time')

        if not exclude_filters and not include_filters:
            include_filters = ['*']

        self.mode = mode
        self.parser = parser
        self.checkers = checkers
        self.reporters = reporters
        self.verbose = verbose
        self.include_filters = include_filters
        self.exclude_filters = exclude_filters

    @staticmethod
    def __in_filter(filters, path):
        if not filters:
            return False

        for filter_ in filters:
            if fnmatch.fnmatch(path, filter_):
                return True
        return False

    def __process_file(self, root_path, full_path):
        if self.verbose:
            print('Processing {}'.format(full_path))

        diagnostics = []
        ast = self.parser.parse_file(full_path)

        for checker in self.checkers:
            if getattr(checker, 'process_file', None):
                results = checker.process_file(ast=ast,
                                               root_directory=root_path,
                                               filename=os.path.relpath(full_path, root_path))
                for result in results:
                    diagnostics.append(create_full_diagnostic(
                        result, full_path, checker.__module__))

        for reporter in self.reporters:
            reporter.report(diagnostics)

    def traverse(self, path):
        root_cmake = None
        root_path = None
        for file in os.listdir(path):
            if file == 'CMakeLists.txt':
                root_cmake = os.path.join(os.path.abspath(path), file)
                root_path = os.path.dirname(root_cmake)

        if not root_cmake:
            raise RuntimeError(
                'CMakeLists.txt has not been found in {}'.format(path))

        for dirname, _, filenames in os.walk(path):
            diagnostics = []
            for checker in self.checkers:
                if getattr(checker, 'process_directory', None):
                    results = checker.process_directory(root_directory=root_path,
                                                        dirname=dirname)
                    diagnostics += results

            for reporter in self.reporters:
                reporter.report(diagnostics)

            for filename in filenames:
                full_path = os.path.join(dirname, filename)

                if Traverser.__in_filter(self.exclude_filters, full_path):
                    continue

                if self.include_filters:
                    if not Traverser.__in_filter(self.include_filters, full_path):
                        continue

                if not re.findall(r'(CMakeLists\.txt|.*\.cmake)$', filename):
                    continue

                self.__process_file(root_path, full_path)

        diagnostics = []
        for checker in self.checkers:
            if getattr(checker, 'end_processing', None):
                results = checker.end_processing()
                diagnostics += results

        for reporter in self.reporters:
            reporter.report(diagnostics)
            reporter.end()
