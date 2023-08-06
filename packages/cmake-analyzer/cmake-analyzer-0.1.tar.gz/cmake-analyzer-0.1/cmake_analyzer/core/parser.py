import tatsu
import tatsu.model


class CMakeParser:
    def __init__(self, grammar_file):
        with open(grammar_file, 'r') as file_handle:
            grammar = file_handle.read()
        self.model = tatsu.compile(grammar, name='CMake')

    def parse_file(self, file):
        with open(file, 'r') as file_handle:
            content = file_handle.read()

        ast = self.model.parse(content)
        output_ast = []
        for line in ast:
            if isinstance(line, list) or isinstance(line, str):
                continue
            output_ast.append(line)
        return output_ast
