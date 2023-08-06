from collections import namedtuple

SimpleDiagnostic = namedtuple('SimpleDiagnostic', ['line', 'message'])
Diagnostic = namedtuple('Diagnostic', ['file', 'line', 'message', 'module'])


def create_diagnostic(node,
                      message: str) -> SimpleDiagnostic:
    parse_info = node['parseinfo']
    return SimpleDiagnostic(parse_info.line + 1, message)


def create_full_diagnostic(simple_diagnostic: SimpleDiagnostic,
                           abs_file_path: str,
                           module_name: str) -> Diagnostic:
    return Diagnostic(abs_file_path, simple_diagnostic.line, simple_diagnostic.message, module_name)
