"""Module for Grammar class."""

from ..compiler.tokens.token import Token

type SyntaxList = list[Token | tuple[Token, SyntaxList]]


class Grammar:
    """Class representing a grammar."""

    def __init__(
        self,
        lineno: int,
        name: str,
        tokens: SyntaxList,
        inherits: str | None = None,
    ) -> None:
        """Init of Grammar."""
        self.lineno = lineno
        self.name = name
        self.tokens = tokens
        self.inherits = inherits

    def __repr__(self) -> str:
        name = self.__class__.__name__
        tokens = [token for token in self.tokens]
        return f"<{name} {self.name}({self.inherits}) {tokens}>"
