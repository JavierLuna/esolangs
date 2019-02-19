import unittest

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