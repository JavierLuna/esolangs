import unittest
from io import StringIO
from unittest.mock import patch

from interpreters.bfuck.commands import BFRepetibleCommand, BFBranchCommand, CellPointerIncrementCommand, \
    CellValueIncrementCommand, OpenBranchCommand, ClosingBranchCommand, GetCellValueCommand, SetCellValueCommand, \
    BFCommand
from interpreters.bfuck.environment import BFEnvironment


class BFCommandTest(unittest.TestCase):

    def test_next(self):
        command_1 = BFCommand(None, next=None)
        command_2 = BFCommand(None, next=None)
        command_1.next = command_2
        self.assertEqual(command_1.next, command_2)

    def test_operator_str(self):
        command_1 = BFCommand(None, operator='test')
        self.assertEqual(str(command_1), 'test')

    def test_operator_repr(self):
        command_1 = BFCommand(None, operator='test')
        self.assertEqual(repr(command_1), 'test')

    def test_operator_execute_does_nothing(self):
        command = BFCommand(None)
        command.execute()


class BFBranchCommandTest(unittest.TestCase):

    def test_branch_condition_false(self):
        env = BFEnvironment()
        env.current_cell = 0
        b_command = BFBranchCommand(env)
        self.assertFalse(b_command.branch_condition())

    def test_branch_condition_true(self):
        env = BFEnvironment()
        env.current_cell = 1
        b_command = BFBranchCommand(env)
        self.assertTrue(b_command.branch_condition())

    def test_jump_condition_true(self):
        env = BFEnvironment()
        env.current_cell = 1
        b_command = BFBranchCommand(env, next_true=1, next_false=2)
        self.assertEqual(b_command.next, 1)

    def test_jump_condition_false(self):
        env = BFEnvironment()
        env.current_cell = 0
        b_command = BFBranchCommand(env, next_true=1, next_false=2)
        self.assertEqual(b_command.next, 2)


class BFRepetibleCommandTest(unittest.TestCase):

    def test_add_bfrepetible_commands_positives(self):
        command_1, command_2 = BFRepetibleCommand(None, times=1), BFRepetibleCommand(None, times=1)
        command_3 = command_1 + command_2
        self.assertEqual(command_3.times, 2)

    def test_add_bfrepetible_commands_positive_negative(self):
        command_1, command_2 = BFRepetibleCommand(None, times=1), BFRepetibleCommand(None, times=-1)
        command_3 = command_1 + command_2
        self.assertEqual(command_3.times, 0)

    def test_add_bfrepetible_commands_positive_zero(self):
        command_1, command_2 = BFRepetibleCommand(None, times=1), BFRepetibleCommand(None, times=0)
        command_3 = command_1 + command_2
        self.assertEqual(command_3.times, 1)

    def test_add_bfrepetible_commands_negatives(self):
        command_1, command_2 = BFRepetibleCommand(None, times=-1), BFRepetibleCommand(None, times=-1)
        command_3 = command_1 + command_2
        self.assertEqual(command_3.times, -2)


class CellPointerIncrementCommandTest(unittest.TestCase):

    def test_simple_positive_increment(self):
        env = BFEnvironment()
        current_cell_pointer = env.cell_pointer
        cpi_command = CellPointerIncrementCommand(env)
        cpi_command.execute()
        self.assertEqual(env.cell_pointer, current_cell_pointer + 1)

    def test_simple_negative_increment(self):
        env = BFEnvironment()
        current_cell_pointer = env.cell_pointer
        cpi_command = CellPointerIncrementCommand(env, times=-1)
        cpi_command.execute()
        self.assertEqual(env.cell_pointer, current_cell_pointer - 1)

    def test_no_increment(self):
        env = BFEnvironment()
        current_cell_pointer = env.cell_pointer
        cpi_command = CellPointerIncrementCommand(env, times=0)
        cpi_command.execute()
        self.assertEqual(env.cell_pointer, current_cell_pointer)

    def test_stacked_positive_increment(self):
        env = BFEnvironment()
        current_cell_pointer = env.cell_pointer
        times_increment = 3
        cpi_command = CellPointerIncrementCommand(env, times=times_increment)
        cpi_command.execute()
        self.assertEqual(env.cell_pointer, current_cell_pointer + times_increment)

    def test_stacked_negative_increment(self):
        env = BFEnvironment()
        current_cell_pointer = env.cell_pointer
        times_increment = -3
        cpi_command = CellPointerIncrementCommand(env, times=times_increment)
        cpi_command.execute()
        self.assertEqual(env.cell_pointer, current_cell_pointer + times_increment)

    def test_simple_positive_increment_str_operator(self):
        cpi_command = CellPointerIncrementCommand(None)
        self.assertEqual(str(cpi_command), ">")

    def test_simple_negative_increment_str_operator(self):
        cpi_command = CellPointerIncrementCommand(None, times=-1)
        self.assertEqual(str(cpi_command), "<")

    def test_stacked_positive_increment_str_operator(self):
        times = 3
        cpi_command = CellPointerIncrementCommand(None, times=times)
        self.assertEqual(str(cpi_command), ">" * times)

    def test_stacked_negative_increment_str_operator(self):
        times = 3
        cpi_command = CellPointerIncrementCommand(None, times=-1 * times)
        self.assertEqual(str(cpi_command), "<" * times)

    def test_simple_no_increment_str_operator(self):
        cpi_command = CellPointerIncrementCommand(None, times=0)
        self.assertEqual(str(cpi_command), "")

    def test_simple_positive_increment_repr_operator(self):
        cpi_command = CellPointerIncrementCommand(None)
        self.assertEqual(repr(cpi_command), ">")

    def test_simple_negative_increment_repr_operator(self):
        cpi_command = CellPointerIncrementCommand(None, times=-1)
        self.assertEqual(repr(cpi_command), "<")

    def test_stacked_positive_increment_repr_operator(self):
        times = 3
        cpi_command = CellPointerIncrementCommand(None, times=times)
        self.assertEqual(repr(cpi_command), ">" * times)

    def test_stacked_negative_increment_repr_operator(self):
        times = 3
        cpi_command = CellPointerIncrementCommand(None, times=-1 * times)
        self.assertEqual(repr(cpi_command), "<" * times)

    def test_simple_no_increment_repr_operator(self):
        cpi_command = CellPointerIncrementCommand(None, times=0)
        self.assertEqual(repr(cpi_command), "")


class CellValueIncrementCommandTest(unittest.TestCase):
    def test_simple_positive_increment(self):
        env = BFEnvironment()
        current_cell_value = env.current_cell
        cpi_command = CellValueIncrementCommand(env)
        cpi_command.execute()
        self.assertEqual(env.current_cell, current_cell_value + 1)

    def test_simple_negative_increment(self):
        env = BFEnvironment()
        current_cell_value = env.current_cell
        cpi_command = CellValueIncrementCommand(env, times=-1)
        cpi_command.execute()
        self.assertEqual(env.current_cell, current_cell_value - 1)

    def test_no_increment(self):
        env = BFEnvironment()
        current_cell_value = env.current_cell
        cpi_command = CellValueIncrementCommand(env, times=0)
        cpi_command.execute()
        self.assertEqual(env.current_cell, current_cell_value)

    def test_stacked_positive_increment(self):
        env = BFEnvironment()
        current_cell_value = env.current_cell
        times_increment = 3
        cpi_command = CellValueIncrementCommand(env, times=times_increment)
        cpi_command.execute()
        self.assertEqual(env.current_cell, current_cell_value + times_increment)

    def test_stacked_negative_increment(self):
        env = BFEnvironment()
        current_cell_value = env.current_cell
        times_increment = -3
        cpi_command = CellValueIncrementCommand(env, times=times_increment)
        cpi_command.execute()
        self.assertEqual(env.current_cell, current_cell_value + times_increment)

    def test_simple_positive_increment_str_operator(self):
        cpi_command = CellValueIncrementCommand(None)
        self.assertEqual(str(cpi_command), "+")

    def test_simple_negative_increment_str_operator(self):
        cpi_command = CellValueIncrementCommand(None, times=-1)
        self.assertEqual(str(cpi_command), "-")

    def test_simple_no_increment_str_operator(self):
        cpi_command = CellValueIncrementCommand(None, times=0)
        self.assertEqual(str(cpi_command), "")


class GetCellValueCommandTest(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_cell_value(self, mock_stdout):
        env = BFEnvironment()
        env.current_cell = ord("a")
        gc_command = GetCellValueCommand(env)
        gc_command.execute()
        self.assertEqual(mock_stdout.getvalue(), "a")


class SetCellValueCommandTest(unittest.TestCase):

    @patch('sys.stdin.read')
    def test_set_cell_value(self, mock_stdin):
        mock_stdin.return_value = 'a'
        env = BFEnvironment()
        env.current_cell = ord("c")
        gc_command = SetCellValueCommand(env)
        gc_command.execute()
        self.assertEqual(env.current_cell, ord("a"))


class OpenBranchCommandTest(unittest.TestCase):

    def test_assign_companion(self):
        ob_command = OpenBranchCommand(None, companion=None)
        ob_command.companion = 1
        self.assertEqual(ob_command.companion, 1)

    def test_assign_no_jump(self):
        ob_command = OpenBranchCommand(None, next=2)
        ob_command.no_jump = 1
        self.assertEqual(ob_command.no_jump, 1)

    def test_next_true_command(self):
        env = BFEnvironment()
        env.current_cell = 1
        ob_command = OpenBranchCommand(env, companion=1, next=2)
        self.assertEqual(ob_command.next, 2)

    def test_next_false_command(self):
        env = BFEnvironment()
        env.current_cell = 0
        ob_command = OpenBranchCommand(env, companion=1, next=2)
        self.assertEqual(ob_command.companion, 1)


class ClosingBranchCommandTest(unittest.TestCase):

    def test_assign_companion(self):
        cb_command = ClosingBranchCommand(None, companion=None)
        cb_command.companion = 1
        self.assertEqual(cb_command.companion, 1)

    def test_assign_no_jump(self):
        cb_command = ClosingBranchCommand(None, next=2)
        cb_command.no_jump = 1
        self.assertEqual(cb_command.no_jump, 1)

    def test_next_true_command(self):
        env = BFEnvironment()
        env.current_cell = 1
        cb_command = ClosingBranchCommand(env, companion=1, next=2)
        self.assertEqual(cb_command.next, 1)

    def test_next_false_command(self):
        env = BFEnvironment()
        env.current_cell = 0
        cb_command = ClosingBranchCommand(env, companion=1, next=2)
        self.assertEqual(cb_command.companion, 2)
