import sys

from interpreters.bfuck.environment import BFEnvironment
from interpreters.bfuck.grammar import PLUS_SIGN, MINUS_SIGN, GT_COMPARATOR, LT_COMPARATOR, DOT, COMMA, OPEN_BRACKET, \
    CLOSE_BRACKET


class BFCommand:

    def __init__(self, env: BFEnvironment, next: 'BFCommand' = None, operator: str = ""):
        self._operator = operator
        self.env = env
        self._next = next

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, value):
        self._next = value

    def execute(self):
        pass

    @property
    def operator(self):
        return self._operator

    def __repr__(self):
        return self.operator

    def __str__(self):
        return self.operator


class BFRepetibleCommand(BFCommand):

    def __init__(self, env, next=None, operator="", times=0):
        self.times = times
        self._operator_ez = ""
        self._operator_gz = ""
        self._operator_lz = ""
        super().__init__(env, next=next, operator=operator)

    @property
    def operator(self):
        if self.times == 0:
            return self._operator_ez
        elif self.times > 0:
            return self._operator_gz
        else:
            return self._operator_lz

    def __repr__(self):
        return self.operator * abs(self.times)

    def __str__(self):
        return self.operator * abs(self.times)

    def __add__(self, other):
        self.times += other.times
        return self


class BFBranchCommand(BFCommand):

    def __init__(self, env: BFEnvironment, companion: BFCommand = None, no_jump: BFCommand = None, operator="["):
        self.companion = companion
        self.no_jump = no_jump
        super().__init__(env, operator=operator)

    def branch_condition(self):
        return bool(self.env.current_cell)

    @property
    def next(self):
        next = self.no_jump
        if self.branch_condition():
            # Ohhh shit! This guy's jumping!
            next = self.companion
            if isinstance(self.companion, BFBranchCommand):
                next = next.no_jump
        return next


class CellPointerIncrementCommand(BFRepetibleCommand):

    def __init__(self, env: BFEnvironment, times: int = 1, next=None, operator='+'):
        super().__init__(env, times=times, next=next, operator=operator)
        self._operator_gz = ">"
        self._operator_lz = "<"

    def execute(self):
        self.env.cell_pointer += self.times


class CellValueIncrementCommand(BFRepetibleCommand):

    def __init__(self, env: BFEnvironment, times: int = 1, next=None, operator='>'):
        super().__init__(env, times=times, next=next, operator=operator)
        self._operator_gz = "+"
        self._operator_lz = "-"

    def execute(self):
        self.env.current_cell += self.times


class SetCellValueCommand(BFCommand):

    def __init__(self, env, next=None):
        super().__init__(env, operator=",", next=next)

    def execute(self):
        char = "\n"
        while char == "\n":
            char = sys.stdin.read(1)
        self.env.current_cell = ord(char)


class GetCellValueCommand(BFCommand):

    def __init__(self, env, next=None):
        super().__init__(env, operator=".", next=next)

    def execute(self):
        print(chr(self.env.current_cell), flush=False, end="")


class OpenBranchCommand(BFBranchCommand):

    def __init__(self, env, **kwargs):
        super().__init__(env, operator='[', **kwargs)

    def branch_condition(self):
        return not bool(self.env.current_cell)


class ClosingBranchCommand(BFBranchCommand):

    def __init__(self, env, **kwargs):
        super().__init__(env, operator="]", **kwargs)

    def branch_condition(self):
        return bool(self.env.current_cell)


TOKEN_TO_COMMAND = {PLUS_SIGN: CellValueIncrementCommand,
                    MINUS_SIGN: lambda env: CellValueIncrementCommand(env, times=-1),
                    GT_COMPARATOR: CellPointerIncrementCommand,
                    LT_COMPARATOR: lambda env: CellPointerIncrementCommand(env, times=-1),
                    DOT: GetCellValueCommand,
                    COMMA: SetCellValueCommand,
                    OPEN_BRACKET: OpenBranchCommand,
                    CLOSE_BRACKET: ClosingBranchCommand
                    }
