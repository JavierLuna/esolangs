import unittest
from io import StringIO
from unittest.mock import patch

from interpreters import BrainFuckInterpreter


class TestBFInterpreterUnitary(unittest.TestCase):

    def test_ast_caching_no_execution(self):
        interpreter = BrainFuckInterpreter("-.-.-.-.-.-.-.-")
        self.assertIsNotNone(interpreter.env)
        self.assertFalse(interpreter._code_is_dirty)
        self.assertIsNone(interpreter._cached_ast)

    def test_ast_caching_execute_once(self):
        interpreter = BrainFuckInterpreter("+")
        self.assertIsNotNone(interpreter.env)
        self.assertIsNone(interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)
        interpreter.execute()
        self.assertIsNotNone(interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)

    def test_ast_caching_execute_twice(self):
        interpreter = BrainFuckInterpreter("+")
        self.assertIsNotNone(interpreter.env)
        self.assertIsNone(interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)
        interpreter.execute()
        self.assertIsNotNone(interpreter._cached_ast)
        cached_ast = interpreter._cached_ast
        self.assertFalse(interpreter._code_is_dirty)
        interpreter.execute()
        self.assertIs(cached_ast, interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)

    def test_ast_caching_code_dirty(self):
        interpreter = BrainFuckInterpreter("+")
        self.assertIsNotNone(interpreter.env)
        self.assertIsNone(interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)
        interpreter.execute()
        self.assertIsNotNone(interpreter._cached_ast)
        cached_ast = interpreter._cached_ast
        self.assertFalse(interpreter._code_is_dirty)
        interpreter.execute()
        self.assertIs(cached_ast, interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)

        interpreter.code = "-"
        self.assertTrue(interpreter._code_is_dirty)
        self.assertEqual(cached_ast, interpreter._cached_ast)

        interpreter.execute()
        self.assertIsNot(cached_ast, interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)

    def test_ast_code_clean_if_same_value(self):
        interpreter = BrainFuckInterpreter("+")
        self.assertIsNotNone(interpreter.env)
        self.assertIsNone(interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)
        interpreter.execute()
        self.assertIsNotNone(interpreter._cached_ast)
        cached_ast = interpreter._cached_ast
        self.assertFalse(interpreter._code_is_dirty)
        interpreter.execute()
        self.assertIs(cached_ast, interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)

        interpreter.code = "+"
        self.assertFalse(interpreter._code_is_dirty)
        self.assertEqual(cached_ast, interpreter._cached_ast)

        interpreter.execute()
        self.assertIs(cached_ast, interpreter._cached_ast)
        self.assertFalse(interpreter._code_is_dirty)


class TestBFPrograms(unittest.TestCase):

    def test_add_two_cells(self):
        code = "++++>+++++<[>+<-]"
        interpreter = BrainFuckInterpreter(code)
        interpreter.execute()
        self.assertEqual(interpreter.env.current_cell, 0)
        interpreter.env.cell_pointer += 1
        self.assertEqual(interpreter.env.current_cell, 9)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_char(self, mock_stdout):
        code = "+" * ord("a") + "."
        interpreter = BrainFuckInterpreter(code)
        interpreter.execute()
        self.assertEqual(mock_stdout.getvalue(), "a")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin.read')
    def test_uppercase_char(self, mock_stdin, mock_stdout):
        mock_stdin.return_value = 'a'
        code = "," + "-" * 32 + "."
        interpreter = BrainFuckInterpreter(code)
        interpreter.execute()
        self.assertEqual(mock_stdout.getvalue(), "A")

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_hello_world(self, mock_stdout):
        code = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++" \
               ".>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
        interpreter = BrainFuckInterpreter(code)
        interpreter.execute()
        self.assertEqual(mock_stdout.getvalue(), "Hello World!\n")
