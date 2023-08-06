from typing import List

from cmake_analyzer.core.reporter_base import Diagnostic

class SimpleReporter:
    @staticmethod
    def report(iterable: List[Diagnostic]):
        for diag in iterable:
            print('{}:{} - {} [{}]'.format(diag.file, diag.line, diag.message, diag.module))

    @staticmethod
    def end():
        pass
