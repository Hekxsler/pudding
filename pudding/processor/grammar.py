"""Module for Grammar class."""

from typing import Iterator
from ..tokens.token import Token

type TokenList = list[Token | tuple[Token, TokenList]]

class Grammar:
    """Class representing a grammar.
    
    :var lineno: Line number the grammar is defined in.
    :var name: Name of the grammar.
    :var tokens: Tokens in this grammar.
    :var inherits: Name of the inherited grammar or None.
    """

    def __init__(
        self,
        lineno: int,
        name: str,
        tokens: TokenList,
        inherits: str | None = None,
    ) -> None:
        """Init of Grammar.

        :param lineno: Line number the grammar is defined in.
        :param name: Name of the grammar.
        :param tokens: Tokens in this grammar.
        :param inherits: Name of the inherited grammar or None.
        """
        self.lineno = lineno
        self.name = name
        self.tokens = tokens
        self.inherits = inherits
    
    def iter_tokens(self) -> Iterator[Token | tuple[Token, TokenList]]:
        """Return iterator for tokens."""
        return self.tokens.__iter__()

    def __repr__(self) -> str:
        """Return string representation of this object."""
        name = self.__class__.__name__
        tokens = [token for token in self.tokens]
        return f"<{name} {self.name}({self.inherits}) {tokens}>"
