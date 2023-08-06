from cmake_analyzer.core import module_base
from cmake_analyzer.core.reporter_base import create_diagnostic


class DeprecatedLinkPrefixChecker(module_base.SingleFileChecker):
    error = "Usage of LINK_PUBLIC/LINK_PRIVATE with target_link_libraries is deprecated."

    @staticmethod
    def __find_diag(node):
        command_name = node['name'].lower()
        if command_name != 'target_link_libraries':
            return False

        for arg in node['args']:
            # this is a quoted arg which could not be LINK_PRIVATE or LINK_PUBLIC
            if isinstance(arg['arg'], list):
                continue
            arg_val = arg['arg'].lower()
            if arg_val in ['link_public', 'link_private']:
                return True
        return False

    @staticmethod
    def process_file(ast, root_directory, filename):
        diags = []

        for node in ast:
            if DeprecatedLinkPrefixChecker.__find_diag(node):
                diag = create_diagnostic(
                    node, DeprecatedLinkPrefixChecker.error)
                diags.append(diag)

        return diags
