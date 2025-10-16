"""Module defining the parser class reading the pud file."""

import logging
from collections.abc import Sequence
from pathlib import Path

from ..processor.grammar import Grammar, TokenList
from ..tokens.statements import Define, FromImport
from ..tokens.statements import Grammar as GrammarStmt
from ..tokens.statements import Import
from ..tokens.token import Token
from ..tokens.util import INDENTATION_RE
from .util import DEFAULT_TOKENS

COMMENT_CHAR = "#"
INDENT_SPACES = 4

logger = logging.getLogger(__name__)

type Syntax = list[Define | FromImport | Import | Grammar]


class Compiler:
    """Base Compiler class."""

    source_path: Path

    def __init__(self, tokens: Sequence[type[Token]] | None = None) -> None:
        """Init of Compiler class.

        :param tokens: Token classes needed to compile. If is None use default tokens.
        """
        default_tokens: Sequence[type[Token]] = DEFAULT_TOKENS
        if tokens is None:
            tokens = default_tokens
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

    def _import(self, path: str) -> Syntax:
        """Parse the syntax from another file.

        :param path: Path of the file to import.
        """
        logger.debug("Importing %s...", path)
        if hasattr(self, "source_path"):
            base_dir = self.source_path.parent
        else:
            raise ImportError("Can not import without a source file.")
        import_file = base_dir / f"{path}.pud"
        try:
            return self.compile_file(import_file)
        except FileNotFoundError as e:
            raise ImportError(f"No file {import_file}") from e

    def _from_import(self, importobj: str, importpath: str) -> Define | Grammar:
        """Get grammar or define statement from another file.

        :param importobj: Name of the grammar or variable to import.
        :param importpath: Path of the .pud file.
        :returns: The grammar or define statement.
        :raises ImportError: If no grammar or variable exists with the given name.
        """
        for token in self._import(importpath):
            if isinstance(token, Grammar) and token.name == importobj:
                return token
            if isinstance(token, Define) and token.values[0].value == importobj:
                return token
        raise ImportError(
            f"No grammar or variable with name '{importobj}' in {importpath}.pud"
        )

    def _compile_syntax(self, syntax: TokenList) -> Syntax:
        """Convert some statements into models for better execution.

        :param syntax: Syntax to convert.
        :returns: The converted Syntax.
        """

        def create_grammar(
            token: GrammarStmt, sub_tokens: TokenList, inherits: str = ""
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
        sub_tokens: TokenList = []
        for token in syntax:
            if isinstance(token, tuple):
                token, sub_tokens = token
            match token:
                case Define():
                    new_syntax.append(token)
                case FromImport():
                    importpath = token.values[0].value
                    importobj = token.values[1].value
                    new_syntax.append(
                        self._from_import(importobj, importpath)
                    )
                case GrammarStmt():
                    new_syntax.append(create_grammar(token, sub_tokens))
                case Import():
                    importpath = token.values[0].value
                    new_syntax.extend(self._import(importpath))
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

    def compile_file(self, file: Path, encoding: str = "utf-8") -> Syntax:
        """Produce executable syntax object from pud file.

        :param file: Path of the syntax file.
        :return: Tuple with syntax and last line number.
        """
        logger.debug("Compiling %s", file)
        self.source_path = file
        content = open(file, "r", encoding=encoding).read()
        return self.compile(content)
