from cmake_analyzer.core import module_base
from cmake_analyzer.core.reporter_base import create_diagnostic


class AddDefinitionsFinder(module_base.SingleFileChecker):
    error = 'Do not use add_definitions() command. It was superseeded by add_compile_definitions/include_directories/add_compile_options. Use these commands instead.'

    @staticmethod
    def process_file(ast, root_directory, filename):
        diags = []

        for node in ast:
            if node['name'].lower() == 'add_definitions':
                diags.append(create_diagnostic(
                    node, AddDefinitionsFinder.error))

        return diags
