from cmake_analyzer.core import module_base
from cmake_analyzer.core.reporter_base import create_diagnostic


class DeprecatedQt5UseModulesChecker(module_base.SingleFileChecker):
    error = "qt5_use_modules is deprecated. Use target_link_libraries with Qt:: IMPORTED targets instead."

    @staticmethod
    def process_file(ast, root_directory, filename):
        diags = []

        for node in ast:
            if node['name'].lower() == 'qt5_use_modules':
                diag = create_diagnostic(
                    node, DeprecatedQt5UseModulesChecker.error)
                diags.append(diag)

        return diags
