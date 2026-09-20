from dataclasses import dataclass


@dataclass
class Citation:
    law: str
    article: str


@dataclass
class GeneratedAnswer:
    answer: str
    citations: list[Citation]
    grounded: bool