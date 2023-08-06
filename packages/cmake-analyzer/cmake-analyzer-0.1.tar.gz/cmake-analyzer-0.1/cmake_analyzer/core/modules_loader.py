import os
import importlib
import sys
import inspect
import fnmatch

from .module_base import SingleFileChecker


class ModulesLoader:
    def __init__(self, modules_paths, filters=['*']):
        self.modules_paths = modules_paths
        self.modules = []
        self.checkers = []
        self.filters = filters
        for path in self.modules_paths:
            self.__load_modules(path)

    @staticmethod
    def __check_imported_checker(checker):
        for attribute in ['process_directory', 'process_file', 'end_processing']:
            attr = getattr(checker, attribute, None)
            if attr and callable(attr):
                return True
        return False

    def __load_checkers(self, module):
        classes = inspect.getmembers(module, inspect.isclass)
        for _, class_type in classes:
            if class_type.__bases__[0] == SingleFileChecker:
                class_object = class_type()
                if ModulesLoader.__check_imported_checker(class_object):
                    self.checkers.append(class_object)

    def __match_filters(self, filename):
        for filter_ in self.filters:
            match_result = fnmatch.fnmatch(filename, filter_)
            if not match_result:
                return False
        return True

    def __load_modules(self, path):
        sys.path.append(path)
        for filename in os.listdir(path):
            if not self.__match_filters(filename):
                continue

            if not filename.endswith('.py'):
                continue

            module = importlib.import_module(os.path.splitext(filename)[0])
            self.modules.append(module)
            self.__load_checkers(module)

    @property
    def loaded_modules(self):
        return self.modules

    @property
    def loaded_checkers(self):
        return self.checkers
