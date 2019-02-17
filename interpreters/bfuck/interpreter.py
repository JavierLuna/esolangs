from interpreters.bfuck.environment import BFEnvironment
from interpreters.bfuck.ast_builder import BEASTBuilder


class BrainFuckInterpreter:

    def __init__(self, code):
        self._code = code
        self._code_is_dirty = False
        self._cached_ast = None
        self.env = BFEnvironment(code)

    def execute(self):
        next_command = self._get_ast()
        while next_command is not None:
            next_command.execute()
            next_command = next_command.next

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code_is_dirty = True
        self._code = value

    def _get_ast(self):
        if self._code_is_dirty or self._cached_ast is None:
            b = BEASTBuilder(self.code, self.env)
            self._cached_ast = b.build_ast()
            self._code_is_dirty = False
        return self._cached_ast
