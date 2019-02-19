import unittest

from interpreters.bfuck.ast_builder import BEASTBuilder
from interpreters.bfuck.commands import CellValueIncrementCommand, CellPointerIncrementCommand, OpenBranchCommand, \
    ClosingBranchCommand, GetCellValueCommand, SetCellValueCommand, BFCommand
from interpreters.bfuck.environment import BFEnvironment


class TestBEASTBuilderGetToken(unittest.TestCase):

    def setUp(self):
        self.env = BFEnvironment()
        self.beast_builder = BEASTBuilder("", self.env)

    def test_get_command_from_token_plus(self):
        command = self.beast_builder._get_command_from_token('+')
        self.assertIsInstance(command, CellValueIncrementCommand)
        self.assertEqual(command.times, 1)

    def test_get_command_from_token_minus(self):
        command = self.beast_builder._get_command_from_token('-')
        self.assertIsInstance(command, CellValueIncrementCommand)
        self.assertEqual(command.times, -1)

    def test_get_command_from_token_lt(self):
        command = self.beast_builder._get_command_from_token('<')
        self.assertIsInstance(command, CellPointerIncrementCommand)
        self.assertEqual(command.times, -1)

    def test_get_command_from_token_gt(self):
        command = self.beast_builder._get_command_from_token('>')
        self.assertIsInstance(command, CellPointerIncrementCommand)
        self.assertEqual(command.times, 1)

    def test_get_command_from_open_branch(self):
        command = self.beast_builder._get_command_from_token('[')
        self.assertIsInstance(command, OpenBranchCommand)

    def test_get_command_from_closed_branch(self):
        command = self.beast_builder._get_command_from_token(']')
        self.assertIsInstance(command, ClosingBranchCommand)

    def test_get_command_from_dot(self):
        command = self.beast_builder._get_command_from_token('.')
        self.assertIsInstance(command, GetCellValueCommand)

    def test_get_command_from_comma(self):
        command = self.beast_builder._get_command_from_token(',')
        self.assertIsInstance(command, SetCellValueCommand)


class TestBEASTBuilderGeneratePreAST(unittest.TestCase):

    def setUp(self):
        self.env = BFEnvironment()

    def test_pre_ast_increment(self):
        builder = BEASTBuilder("+", self.env)
        pre_ast = builder._pre_build_ast()
        command = pre_ast[0]
        self.assertIsInstance(command, CellValueIncrementCommand)

    def test_pre_ast_two_increments(self):
        builder = BEASTBuilder("+-", self.env)
        pre_ast = builder._pre_build_ast()
        command_1, command_2 = pre_ast
        self.assertIsInstance(command_1, CellValueIncrementCommand)
        self.assertIsInstance(command_2, CellValueIncrementCommand)


class TestBEASTBuilderChainAst(unittest.TestCase):

    def get_chained_ast(self, code):
        env = BFEnvironment()
        builder = BEASTBuilder(code, env)
        pre_ast = builder._pre_build_ast()
        chained_ast = builder._chain_ast(pre_ast)
        return chained_ast

    def test_chain_different_commands_no_branches(self):
        chained_ast = self.get_chained_ast("+>")
        self.assertIsInstance(chained_ast, CellValueIncrementCommand)
        self.assertIsNotNone(chained_ast.next)
        self.assertIsInstance(chained_ast.next, CellPointerIncrementCommand)
        self.assertIsNone(chained_ast.next.next)

    def test_chain_cell_value_increments(self):
        chained_ast = self.get_chained_ast("++")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellValueIncrementCommand)
        self.assertEqual(chained_ast.times, 2)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_value_decrements(self):
        chained_ast = self.get_chained_ast("--")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellValueIncrementCommand)
        self.assertEqual(chained_ast.times, -2)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_value_increment_decrement(self):
        chained_ast = self.get_chained_ast("+-")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellValueIncrementCommand)
        self.assertEqual(chained_ast.times, 0)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_pointer_increments(self):
        chained_ast = self.get_chained_ast(">>")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellPointerIncrementCommand)
        self.assertEqual(chained_ast.times, 2)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_pointer_decrements(self):
        chained_ast = self.get_chained_ast("<<")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellPointerIncrementCommand)
        self.assertEqual(chained_ast.times, -2)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_pointer_increment_decrement(self):
        chained_ast = self.get_chained_ast("><")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellPointerIncrementCommand)
        self.assertEqual(chained_ast.times, 0)
        self.assertIsNone(chained_ast.next)

    def test_no_multiple_chain(self):
        chained_ast = self.get_chained_ast(">-.+,<")
        self.assertIsNotNone(chained_ast)
        self.assertIsInstance(chained_ast, CellPointerIncrementCommand)
        self.assertEqual(chained_ast.times, 1)
        minus_command = chained_ast.next
        self.assertIsNotNone(minus_command)
        self.assertIsInstance(minus_command, CellValueIncrementCommand)
        self.assertEqual(minus_command.times, -1)
        dot_command = minus_command.next
        self.assertIsNotNone(dot_command)
        self.assertIsInstance(dot_command, GetCellValueCommand)
        plus_command = dot_command.next
        self.assertIsNotNone(plus_command)
        self.assertIsInstance(plus_command, CellValueIncrementCommand)
        self.assertEqual(plus_command.times, 1)
        comma_command = plus_command.next
        self.assertIsNotNone(comma_command)
        self.assertIsInstance(comma_command, SetCellValueCommand)
        lt_command = comma_command.next
        self.assertIsNotNone(lt_command)
        self.assertIsInstance(lt_command, CellPointerIncrementCommand)
        self.assertEqual(lt_command.times, -1)
        self.assertIsNone(lt_command.next)

    def test_chain_open_branch_next(self):
        chained_ast = self.get_chained_ast("[-")
        self.assertIsNotNone(chained_ast)
        self.assertIsInstance(chained_ast, OpenBranchCommand)
        minus_command = chained_ast.no_jump
        self.assertIsNotNone(minus_command)
        self.assertIsInstance(minus_command, CellValueIncrementCommand)
        self.assertIsNone(minus_command.next)

    def test_chain_open_close_branch(self):
        chained_ast = self.get_chained_ast("[-]")
        self.assertIsNotNone(chained_ast)
        self.assertIsInstance(chained_ast, OpenBranchCommand)
        minus_command = chained_ast.no_jump
        closing_command = chained_ast.companion
        self.assertIsNotNone(minus_command)
        self.assertIsNotNone(closing_command)
        self.assertIsInstance(minus_command, CellValueIncrementCommand)
        self.assertIsInstance(closing_command, ClosingBranchCommand)
        self.assertIsNone(closing_command.no_jump)

    def test_chain_multiple_branches(self):
        open_branch1 = self.get_chained_ast("[[]]")
        self.assertIsNotNone(open_branch1)
        self.assertIsInstance(open_branch1, OpenBranchCommand)
        open_branch2 = open_branch1.no_jump
        self.assertIsNotNone(open_branch2)
        self.assertIsInstance(open_branch2, OpenBranchCommand)
        closing_branch1 = open_branch2.no_jump
        self.assertIsNotNone(closing_branch1)
        self.assertIsInstance(closing_branch1, ClosingBranchCommand)
        closing_branch2 = closing_branch1.no_jump
        self.assertIsNotNone(closing_branch2)
        self.assertIsInstance(closing_branch2, ClosingBranchCommand)
        self.assertIsNone(closing_branch2.no_jump)

        self.assertIs(open_branch1.companion, closing_branch2)
        self.assertIs(closing_branch2.companion, open_branch1)
        self.assertIs(open_branch2.companion, closing_branch1)
        self.assertIs(closing_branch1.companion, open_branch2)


class TestBEASTBuilderBuildAst(unittest.TestCase):

    def build_ast(self, code):
        env = BFEnvironment()
        builder = BEASTBuilder(code, env)
        ast = builder.build_ast()
        return ast

    def test_chain_different_commands_no_branches(self):
        chained_ast = self.build_ast("+>")
        self.assertIsInstance(chained_ast, CellValueIncrementCommand)
        self.assertIsNotNone(chained_ast.next)
        self.assertIsInstance(chained_ast.next, CellPointerIncrementCommand)
        self.assertIsNone(chained_ast.next.next)

    def test_chain_cell_value_increments(self):
        chained_ast = self.build_ast("++")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellValueIncrementCommand)
        self.assertEqual(chained_ast.times, 2)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_value_decrements(self):
        chained_ast = self.build_ast("--")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellValueIncrementCommand)
        self.assertEqual(chained_ast.times, -2)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_value_increment_decrement(self):
        chained_ast = self.build_ast("+-")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellValueIncrementCommand)
        self.assertEqual(chained_ast.times, 0)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_pointer_increments(self):
        chained_ast = self.build_ast(">>")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellPointerIncrementCommand)
        self.assertEqual(chained_ast.times, 2)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_pointer_decrements(self):
        chained_ast = self.build_ast("<<")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellPointerIncrementCommand)
        self.assertEqual(chained_ast.times, -2)
        self.assertIsNone(chained_ast.next)

    def test_chain_cell_pointer_increment_decrement(self):
        chained_ast = self.build_ast("><")
        self.assertIsNone(chained_ast.next)
        self.assertIsInstance(chained_ast, CellPointerIncrementCommand)
        self.assertEqual(chained_ast.times, 0)
        self.assertIsNone(chained_ast.next)

    def test_no_multiple_chain(self):
        chained_ast = self.build_ast(">-.+,<")
        self.assertIsNotNone(chained_ast)
        self.assertIsInstance(chained_ast, CellPointerIncrementCommand)
        self.assertEqual(chained_ast.times, 1)
        minus_command = chained_ast.next
        self.assertIsNotNone(minus_command)
        self.assertIsInstance(minus_command, CellValueIncrementCommand)
        self.assertEqual(minus_command.times, -1)
        dot_command = minus_command.next
        self.assertIsNotNone(dot_command)
        self.assertIsInstance(dot_command, GetCellValueCommand)
        plus_command = dot_command.next
        self.assertIsNotNone(plus_command)
        self.assertIsInstance(plus_command, CellValueIncrementCommand)
        self.assertEqual(plus_command.times, 1)
        comma_command = plus_command.next
        self.assertIsNotNone(comma_command)
        self.assertIsInstance(comma_command, SetCellValueCommand)
        lt_command = comma_command.next
        self.assertIsNotNone(lt_command)
        self.assertIsInstance(lt_command, CellPointerIncrementCommand)
        self.assertEqual(lt_command.times, -1)
        self.assertIsNone(lt_command.next)

    def test_chain_open_branch_next(self):
        chained_ast = self.build_ast("[-")
        self.assertIsNotNone(chained_ast)
        self.assertIsInstance(chained_ast, OpenBranchCommand)
        minus_command = chained_ast.no_jump
        self.assertIsNotNone(minus_command)
        self.assertIsInstance(minus_command, CellValueIncrementCommand)
        self.assertIsNone(minus_command.next)

    def test_chain_open_close_branch(self):
        chained_ast = self.build_ast("[-]")
        self.assertIsNotNone(chained_ast)
        self.assertIsInstance(chained_ast, OpenBranchCommand)
        minus_command = chained_ast.no_jump
        closing_command = chained_ast.companion
        self.assertIsNotNone(minus_command)
        self.assertIsNotNone(closing_command)
        self.assertIsInstance(minus_command, CellValueIncrementCommand)
        self.assertIsInstance(closing_command, ClosingBranchCommand)
        self.assertIsNone(closing_command.no_jump)

    def test_chain_multiple_branches(self):
        open_branch1 = self.build_ast("[[]]")
        self.assertIsNotNone(open_branch1)
        self.assertIsInstance(open_branch1, OpenBranchCommand)
        open_branch2 = open_branch1.no_jump
        self.assertIsNotNone(open_branch2)
        self.assertIsInstance(open_branch2, OpenBranchCommand)
        closing_branch1 = open_branch2.no_jump
        self.assertIsNotNone(closing_branch1)
        self.assertIsInstance(closing_branch1, ClosingBranchCommand)
        closing_branch2 = closing_branch1.no_jump
        self.assertIsNotNone(closing_branch2)
        self.assertIsInstance(closing_branch2, ClosingBranchCommand)
        self.assertIsNone(closing_branch2.no_jump)

        self.assertIs(open_branch1.companion, closing_branch2)
        self.assertIs(closing_branch2.companion, open_branch1)
        self.assertIs(open_branch2.companion, closing_branch1)
        self.assertIs(closing_branch1.companion, open_branch2)

    def test_build_empty_ast(self):
        ast = self.build_ast("")
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, BFCommand)
        self.assertEqual(type(ast), BFCommand)
        self.assertIsNone(ast.next)
