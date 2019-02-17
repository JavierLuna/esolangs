from typing import Union

from interpreters.bfuck.commands import BFCommand, TOKEN_TO_COMMAND, BFRepetibleCommand, OpenBranchCommand, \
    ClosingBranchCommand, BFBranchCommand

from interpreters.bfuck.grammar import GRAMMAR


class BEASTBuilder:

    def __init__(self, code, env):
        self.env = env
        self.code = [c for c in code if c in GRAMMAR]  # Ignore other chars
        self._pre_processed_ast = []
        self._ast_root = BFCommand(self.env, next=None)

    def build_ast(self):
        self._ast_root = BFCommand(self.env, next=None)
        self._pre_processed_ast.append(self._ast_root)
        self._pre_build_ast()
        self._chain_ast()
        self._pre_processed_ast.pop(0)
        return self._pre_processed_ast[0]

    def _pre_build_ast(self):
        for token in self.code:
            self._pre_processed_ast.append(self._get_command_from_token(token))

    def _chain_ast(self):
        depth = 0
        jump_map = {}
        last_command = self._pre_processed_ast[0]
        for command in self._pre_processed_ast[1:]:
            if type(command) is OpenBranchCommand:
                depth += 1
                jump_map[depth] = command
            elif type(command) is ClosingBranchCommand:
                command.companion = jump_map[depth]
                jump_map[depth].companion = command
                jump_map.pop(depth)
                depth -= 1
            command = self._simple_chain(last_command, command)
            last_command = command

    def _simple_chain(self, last_command: Union[BFCommand, BFRepetibleCommand],
                      current_command: Union[BFCommand, BFRepetibleCommand]):
        last_type = type(last_command)
        current_type = type(current_command)
        if last_type == current_type and isinstance(last_command, BFRepetibleCommand):
            chained_command = last_command + current_command

        elif isinstance(last_command, BFBranchCommand):
            last_command.no_jump = current_command
            chained_command = current_command
        else:
            last_command.next = current_command
            chained_command = current_command
        return chained_command

    def _get_command_from_token(self, token):
        return TOKEN_TO_COMMAND[token](self.env)
