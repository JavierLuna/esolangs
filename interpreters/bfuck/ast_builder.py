from typing import Union

from interpreters.bfuck.commands import BFCommand, TOKEN_TO_COMMAND, BFRepetibleCommand, OpenBranchCommand, \
    ClosingBranchCommand, BFBranchCommand

from interpreters.bfuck.grammar import GRAMMAR


class BEASTBuilder:

    def __init__(self, code, env):
        self.env = env
        self.code = [c for c in code if c in GRAMMAR]  # Ignore other chars

    def build_ast(self):
        if not self.code:
            return BFCommand(self.env)
        pre_ast = self._pre_build_ast()
        ast = self._chain_ast(pre_ast)
        return ast

    def _pre_build_ast(self):
        return [self._get_command_from_token(token) for token in self.code]

    def _chain_ast(self, pre_ast):
        jump_stack = []
        ast_root = last_command = pre_ast.pop(0)
        if type(last_command) is OpenBranchCommand:
            jump_stack.append(last_command)
        while pre_ast:
            current_command = pre_ast.pop(0)
            if type(current_command) is OpenBranchCommand:
                jump_stack.append(current_command)
            elif type(current_command) is ClosingBranchCommand:
                companion = jump_stack.pop()
                current_command.companion = companion
                companion.companion = current_command
            last_command = self._simple_chain(last_command, current_command)
        return ast_root

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
