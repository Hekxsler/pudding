"""Module defining the parser class reading the pud file."""

from collections.abc import Sequence
import logging

from .tokens.functions import FUNCTIONS
from ..processor.grammar import Grammar, SyntaxList
from .tokens.statements import STATEMENTS, Define, Grammar as GrammarStmt, Import
from .tokens.token import Token
from .util import INDENTATION_RE

COMMENT_CHAR = "#"
INDENT_SPACES = 4

logger = logging.getLogger(__name__)

type TokenList = list[Token | tuple[Token, TokenList]]
type Syntax = list[Define | Import | Grammar]


class Compiler:
    """Base Compiler class."""

    def __init__(self, tokens: Sequence[type[Token]] | None = None) -> None:
        """Init of Compiler class.

        :param functions: Functions to check if they exist.
        :param statements: Statements to check if they exist.
        """
        if tokens is None:
            tokens = FUNCTIONS + STATEMENTS
        self.tokens = tokens

    def _parse_indent(self, line: str, lineno: int) -> int:
        """Get indentation of a line."""
        indent = INDENTATION_RE.match(line)
        if not indent:
            return 0
        count = len(indent.group(0))
        if line.startswith("\t"):
            return count
        elif (count / INDENT_SPACES).is_integer():
            return int(count / INDENT_SPACES)
        raise IndentationError(f"Invalid amount of spaces in line {lineno}")

    def _parse_line(self, line: str, lineno: int) -> Token:
        """Read statement or function from a line."""
        line = line.strip()
        for token in self.tokens:
            if token.matches(line):
                return token.from_string(line, lineno)
        raise SyntaxError(f"Invalid statement in line {lineno}")

    def _parse_syntax(
        self, content: str, indent: int = 0, skip_to: int = 0
    ) -> tuple[TokenList, int]:
        """Produce syntax list object from syntax file content.

        :param content: Content of the file to compile.
        :param indent: Indentation level to start from.
        :param skip_to: Line to start from.
        :return: Tuple with syntax and last line number.
        """
        syntax: TokenList = []
        for i, line in enumerate(content.splitlines(True)):
            if not line.strip() or i < skip_to or line.strip().startswith(COMMENT_CHAR):
                continue
            lineno = i + 1
            obj = self._parse_line(line, lineno)
            new_indent = self._parse_indent(line, lineno)
            if indent == new_indent:
                syntax.append(obj)
                continue
            if new_indent > indent:
                last_obj = syntax.pop()
                if isinstance(last_obj, tuple):
                    raise SyntaxError(f"Unexpected indentation in line {lineno}")
                sub_syntax, skip_to = self._parse_syntax(content, new_indent, i)
                syntax.append((last_obj, sub_syntax))
                continue
            if new_indent < indent:
                return syntax, i
        return syntax, len(content.splitlines())

    def _compile_syntax(self, syntax: TokenList) -> Syntax:
        """Convert some statements into models for better execution.

        :param syntax: Syntax to convert.
        """

        def create_grammar(
            token: GrammarStmt, sub_tokens: SyntaxList, inherits: str = ""
        ) -> Grammar:
            """Create a grammar object from a token.

            :param token: The grammar statement.
            :param sub_tokens: Tokens in the grammar.
            :param inherits: Optional name of inherited grammar if not value in token.
            :returns: A Grammar object.
            """
            if len(token.values) == 2:
                inherits = token.values[1].value
            return Grammar(token.lineno, token.values[0].value, sub_tokens, inherits)

        new_syntax: Syntax = []
        sub_tokens = []
        for token in syntax:
            if isinstance(token, tuple):
                token, sub_tokens = token
            match token:
                case Define():
                    new_syntax.append(token)
                case GrammarStmt():
                    new_syntax.append(create_grammar(token, sub_tokens))
                case Import():
                    importpath = token.values[0].value
                    logger.debug("Importing %s...", importpath)
                    filepath = importpath.replace(".", "/")
                    new_syntax.extend(self.compile_file(f"{filepath}.pud"))
                case _:
                    raise SyntaxError(
                        f"Invalid statement outside grammar in line {token.lineno}"
                    )
        return new_syntax

    def compile(self, content: str) -> Syntax:
        """Produce executable syntax object from syntax file.

        :param content: Content of the syntax file.
        :return: Tuple with syntax and last line number.
        """
        syntax, lines = self._parse_syntax(content)
        logger.debug("Parsed %s lines", lines)
        return self._compile_syntax(syntax)

    def compile_file(self, file: str, encoding: str = "utf-8") -> Syntax:
        """Produce executable syntax object from pud file.

        :param file: Path of the syntax file.
        :return: Tuple with syntax and last line number.
        """
        logger.debug("Compiling %s", file)
        content = open(file, "r", encoding=encoding).read()
        return self.compile(content)
