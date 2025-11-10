# instruction.py
class Value:
    S, V, N = "S", "V", "N"

class Instruction:
    def __init__(self, condition: str, imperative: str, goal: str):
        self.condition = condition
        self.imperative = imperative
        self.goal = goal
        self._intended = False
        self._executed = None

    def set_intention(self, intended: bool):
        self._intended = intended

    def mark_executed(self, success: bool):
        self._executed = success

    def evaluate(self) -> str:
        if not self._intended:
            return Value.N
        if self._executed is None:
            raise ValueError("Not executed")
        return Value.S if self._executed else Value.V

    def __repr__(self):
        return f"[{self.condition} → {self.imperative} → {self.goal}]"