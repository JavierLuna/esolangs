import unittest

from interpreters.bfuck.ast_builder import BEASTBuilder
from interpreters.bfuck.commands import CellValueIncrementCommand, CellPointerIncrementCommand, OpenBranchCommand, \
    ClosingBranchCommand, GetCellValueCommand, SetCellValueCommand
from interpreters.bfuck.environment import BFEnvironment


class BEASTBuilderGetTokenTest(unittest.TestCase):

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


class BEASTBuilderGeneratePreASTTest(unittest.TestCase):

    def setUp(self):
        self.env = BFEnvironment()

    def test_pre_ast_increment(self):
        builder = BEASTBuilder("+", self.env)
        builder._pre_build_ast()
        command = builder._pre_processed_ast[0]
        self.assertIsInstance(command, CellValueIncrementCommand)

    def test_pre_ast_two_increments(self):
        builder = BEASTBuilder("+-", self.env)
        builder._pre_build_ast()
        command_1, command_2 = builder._pre_processed_ast
        self.assertIsInstance(command_1, CellValueIncrementCommand)
        self.assertIsInstance(command_2, CellValueIncrementCommand)
