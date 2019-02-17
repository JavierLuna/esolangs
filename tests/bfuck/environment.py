import unittest

from interpreters.bfuck.environment import BFEnvironment


class BFEnvironmentTest(unittest.TestCase):

    def setUp(self):
        self.env = BFEnvironment()

    def test_cells_all_zero(self):
        self.assertFalse(any(self.env.cells))

    def test_pointer_not_zero(self):
        self.assertNotEqual(self.env.cell_pointer, 0)

    def test_environment_reset(self):
        self.env.current_cell = 3
        self.env.reset()
        self.assertEqual(self.env.current_cell, 0)
