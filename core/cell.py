from dataclasses import dataclass


@dataclass
class Cell:
    is_alive: bool = False
