from cmake_analyzer.core import module_base
from cmake_analyzer.core.reporter_base import create_diagnostic


class DeprecatedCommandsChecker(module_base.SingleFileChecker):
    deprecated_commands = ['build_name',
                           'exec_program',
                           'export_library_dependencies',
                           'install_files',
                           'install_programs',
                           'install_targets',
                           'load_command',
                           'make_directory',
                           'output_required_files',
                           'qt_wrap_cpp',
                           'qt_wrap_ui',
                           'remove',
                           'subdir_depends',
                           'subdirs',
                           'use_mangled_mesa',
                           'utility_source',
                           'variable_requires',
                           'write_file']

    @staticmethod
    def process_file(ast, root_directory, filename):
        diags = []

        for node in ast:
            command_name = node['name'].lower()

            if command_name in DeprecatedCommandsChecker.deprecated_commands:
                diag = create_diagnostic(node,
                                         "Command {} is deprecated, consider removing it.".format(command_name))
                diags.append(diag)

        return diags
