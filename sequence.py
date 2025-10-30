# sequence.py
from typing import List
from instruction import Instruction

class Sequence:
    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions

    def srutikrama_order(self):
        return self.instructions.copy()

    def arthakrama_order(self, final_goal: str):
        current = None
        for i in self.instructions:
            if i.goal == final_goal:
                current = i
                break
        if not current:
            return None

        chain = []
        while current:
            chain.append(current)
            prev = None
            for i in self.instructions:
                if i.goal == current.condition:
                    prev = i
                    break
            current = prev
        return chain[::-1]

    def is_valid_arthakrama(self, final_goal: str):
        order = self.arthakrama_order(final_goal)
        return order is not None and len(order) == len(self.instructions)