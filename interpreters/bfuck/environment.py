class BFEnvironment:
    N_CELLS = 30000

    def __init__(self):
        self.cells = [0 for _ in range(self.N_CELLS * 2)]
        self.cell_pointer = int(len(self.cells) / 2)
        self.code_pointer = 0

    def reset(self):
        self.cells = [0 for _ in range(self.N_CELLS * 2)]
        self.cell_pointer = int(len(self.cells) / 2)
        self.code_pointer = 0

    @property
    def current_cell(self):
        return self.cells[self.cell_pointer]

    @current_cell.setter
    def current_cell(self, val):
        self.cells[self.cell_pointer] = val

