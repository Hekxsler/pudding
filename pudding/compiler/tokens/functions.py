"""Module defining functions."""

import re
from typing import NoReturn, Self, TypeVar

from ..datatypes import Regex, String, Varname

from ...processor import PAction
from ...processor.context import Context
from ...processor.triggers import Timing, Trigger, TriggerQueue
from ...writer.xml import Xml
from .token import Token
from ..util import EXP_VAR, STRING_VAR_RE

OPTIONAL_STRING = rf"(?:\, *({String.regex}))?"
_D = TypeVar("_D")

#########################
#      Base classes     #
#########################


class Function(Token):
    """Base class for a function.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    :var min_args: Minimum amount of arguments.
    :var max_args: Maximum amount of arguments.
    """

    min_args = 0
    max_args = 0

    def __init__(self, lineno: int, name: str, values: tuple[str, ...]) -> None:
        err_msg = f"Expected {self.min_args} but got {len(values)}"
        if len(values) < self.min_args:
            raise SyntaxError(f"Missing arguments in line {lineno}. {err_msg}")
        if len(values) > self.max_args:
            raise SyntaxError(f"Too many arguments in line {lineno}. {err_msg}")
        super().__init__(lineno, name, values)

    @classmethod
    def from_string(cls, string: str, lineno: int) -> Self:
        """Create Function object from string.

        :param string: String containing the function.
        """
        function = cls.match_re.search(string)
        if not function:
            raise ValueError("Statement not in given string.")
        name = function.group(1)
        args = cls.value_re.search(function.group(0))
        if not args:
            raise ValueError("No args in function.")
        return cls(lineno, name, args.groups())

    def execute(self, _) -> NoReturn:
        """Function executed by the context.

        :param context: The current context instance.
        """
        raise NotImplementedError()

    def replace_string_vars(self, string: String, context: Context) -> str:
        """Replace variables in a string with the last matched values.

        :param string: String to replace vars in.
        :param context: The current context.
        :returns: The string with replaced values or None if string or last_match of
        context is None.
        """
        if context.reader.last_match is None:
            raise RuntimeError(
                "cannot replace variables, because last regex did not match"
            )
        new_string = string.value
        matches = context.reader.last_match.groups()
        for replace, i in re.findall(STRING_VAR_RE, string.value):
            assert isinstance(replace, str)
            if int(i) > len(matches):
                msg = "ERROR: Not enough matches to replace variables in line"
                raise SyntaxError(f"{msg} {self.lineno}")
            value = replace.replace(f"${i}", matches[int(i)])
            new_string = re.sub(re.escape(replace), value, new_string)
        return new_string

    def get_string(self, index: int) -> String:
        """Get String object in values.

        :param index: Index of the object in values.
        :returns: The String object at the given index.
        :raises TypeError: If object at given index is not of type String.
        """
        value = self.values[index]
        if isinstance(value, String):
            return value
        raise TypeError("Value is not a string.")

    def get_replaced_string(self, index: int, context: Context) -> str:
        """Get a string from values with replaced variables.

        :param index: Index of the string in values.
        :param context: Current context object.
        """
        return self.replace_string_vars(self.get_string(index), context)

    def get_repl_opt_string(
        self, index: int, context: Context, default: _D = None
    ) -> str | _D:
        """Get a optional string with replaced variables.

        :param index: Index of the string in values.
        :param context: Current context object.
        :param default: Default value to return if string does not exist.
        :return: The replaced string or default value if index is invalid.
        """
        try:
            return self.get_replaced_string(index, context)
        except IndexError:
            return default


class Do(Function):
    """Base class for control functions.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    value_types = tuple()

    def execute(self, _) -> NoReturn:
        """Action for control functions."""
        raise NotImplementedError()


class Out(Function):
    """Base class for output generation functions.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 1
    max_args = 2

    def execute(self, _) -> NoReturn:
        """Action for output generation functions."""
        raise NotImplementedError()


#########################
#   Function classes    #
#########################

# Control functions


class Fail(Do):
    """Class for `do.fail` function.
    Like do.say(), but immediately terminates with an error.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 1
    max_args = 1

    match_re = re.compile(rf"(do\.fail)\({String.regex}\)$")
    value_re = re.compile(rf"do\.fail\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> NoReturn:
        """Action of fail function."""
        raise RuntimeError(self.get_replaced_string(0, context))


class Next(Do):
    """Class for `do.next` function.
    Skip the current match and continue with the next match statement without jumping
    back to the top of the current grammar block. This function is rarely used and
    probably not what you want. Instead, use do.skip() in almost all cases,
    unless it is for some performance-specific hacks.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    match_re = re.compile(r"(do\.next)\(\)$")
    value_re = re.compile(r"do\.next\(\)")

    def execute(self, _) -> PAction:
        """Action for next function."""
        return PAction.CONTINUE


class Return(Do):
    """Class for `do.return` function.
    Immediately leave the current grammar block and return to the calling function.
    When used at the top level (i.e. in the input grammar), stop parsing.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    match_re = re.compile(r"(do\.return)\(\)$")
    value_re = re.compile(r"do\.return\(\)")

    def execute(self, _) -> PAction:
        """Action for return function."""
        return PAction.EXIT


class Say(Do):
    """Class for `do.say` function.
    Prints the given string to stdout, with additional debug information.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 1
    max_args = 1

    match_re = re.compile(rf"(do\.say)\({String.regex}\)$")
    value_re = re.compile(rf"do\.say\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Action for say function."""
        print(self.get_replaced_string(0, context))
        return PAction.CONTINUE


class Skip(Do):
    """Class for `do.skip` function.
    Skip the current match and jump back to the top of the current grammar block.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    match_re = re.compile(r"(do\.skip)\(\)$")
    value_re = re.compile(r"do\.skip\(\)")

    def execute(self, _) -> PAction:
        """Action for skip function."""
        return PAction.RESTART


# Output generating functions


class Add(Out):
    """Class for `out.add` function.
    Like out.create(), but appends the string to the text of the existing node
    if it already exists.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    match_re = re.compile(rf"(out\.add)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.add\(({String.regex}){OPTIONAL_STRING}\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Action for add function."""
        path = self.get_replaced_string(0, context)
        value = self.get_repl_opt_string(1, context)
        context.writer.add_element(path, value)
        return PAction.CONTINUE


class AddAttribute(Out):
    """Class for `out.add_attribute` function.
    Adds the attribute with the given name and value to the node with the given path.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 3
    max_args = 3

    match_re = re.compile(
        rf"(out\.add_attribute)\({String.regex}, *{String.regex}, *{String.regex}\)$"
    )
    value_re = re.compile(
        rf"out\.add_attribute\(({String.regex}), *({String.regex}), *({String.regex})\)"
    )
    value_types = (String, String, String)

    def execute(self, context: Context) -> PAction:
        """Action for add_attribute function."""
        context.writer.add_attribute(
            self.get_replaced_string(0, context),
            self.get_replaced_string(1, context),
            self.get_replaced_string(2, context),
        )
        return PAction.CONTINUE


class ClearQueue(Out):
    """Class for `out.clear_queue` function.
    Removes any items from the queue that were previously queued
    using the out.enqueue_*() functions.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 0
    max_args = 0

    match_re = re.compile(r"(out\.clear_queue)\(\)$")
    value_re = re.compile(r"out\.clear_queue\(\)")

    def execute(self, queue: TriggerQueue) -> PAction:
        """Action for clear_queue function."""
        queue.clear_triggers()
        return PAction.CONTINUE


class Create(Out):
    """Class for `out.create` function.
    Creates the leaf node (and attributes) in the given path, regardless of whether or
    not it already exists. In other words, using this function twice will lead to
    duplicates. If the given path contains multiple elements, the parent nodes are only
    created if they do not yet exist. If the second argument is given, the new node is
    also assigned the string as data.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    match_re = re.compile(rf"(out\.create)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.create\(({String.regex}){OPTIONAL_STRING}\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Action for create function."""
        context.writer.create_element(
            self.get_replaced_string(0, context),
            self.get_repl_opt_string(1, context),
        )
        return PAction.CONTINUE


class Enter(Out):
    """Class for `out.enter` function.
    Like out.open(), but only creates the nodes in the given path
    if they do not already exist.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    match_re = re.compile(rf"(out\.enter)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.enter\(({String.regex}{OPTIONAL_STRING})\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Action for enter function."""
        context.writer.enter_path(
            self.get_replaced_string(0, context),
            self.get_repl_opt_string(1, context),
        )
        return PAction.CONTINUE


class EnqueueAfter(Out):
    """Class for `out.enqueue_after` function.
    Like out.enqueue_before(), but is executed after the given regular expression
    matches the input and the next match statement was processed.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 2
    max_args = 3

    match_re = re.compile(
        rf"(out\.enqueue_after)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_after\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )
    value_types = (Regex | Varname, String, String)

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_after function."""
        values = (self.get_replaced_string(1, context),)
        if isinstance(self.get_value(2), String):
            values += (self.get_replaced_string(2, context),)
        context.queue.add_trigger(
            Timing.AFTER,
            Trigger(
                re.compile(self.values[0].value),
                Add(self.lineno, "EnqueuedAdd", values),
            ),
        )
        return PAction.CONTINUE


class EnqueueBefore(Out):
    """Class for `out.enqueue_before` function.
    Like out.add(), but is not immediately executed. Instead, it is executed as soon as
    the given regular expression matches the input, regardless of the grammar in which
    the match occurs.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 2
    max_args = 3

    match_re = re.compile(
        rf"(out\.enqueue_before)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_before\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )
    value_types = (Regex | Varname, String, String)

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_before function."""
        values = (self.get_replaced_string(1, context),)
        if isinstance(self.get_value(2), String):
            values += (self.get_replaced_string(2, context),)
        context.queue.add_trigger(
            Timing.BEFORE,
            Trigger(
                re.compile(self.values[0].value),
                Add(self.lineno, "EnqueuedAdd", values),
            ),
        )
        return PAction.CONTINUE


class EnqueueOnAdd(Out):
    """Class for `out.enqueue_on_add` function.
    Like out.enqueue_before(), but is executed after the given regular expression
    matches the input and the next node is added to the output.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 2
    max_args = 3

    match_re = re.compile(
        rf"(out\.enqueue_on_add)\({EXP_VAR}, *{String.regex}{OPTIONAL_STRING}\)$"
    )
    value_re = re.compile(
        rf"out\.enqueue_on_add\(({EXP_VAR}), *({String.regex}){OPTIONAL_STRING}\)"
    )
    value_types = (Regex | Varname, String, String)

    def execute(self, context: Context) -> PAction:
        """Action for enqueue_on_add function."""
        values = (self.get_replaced_string(1, context),)
        if isinstance(self.get_value(2), String):
            values += (self.get_replaced_string(2, context),)
        context.queue.add_trigger(
            Timing.ON_ADD,
            Trigger(
                re.compile(self.values[0].value),
                Add(self.lineno, "EnqueuedAdd", values),
            ),
        )
        return PAction.CONTINUE


class Open(Out):
    """Class for `out.open` function.
    Like out.create(), but also selects the addressed node, such that the PATH of all
    subsequent function calls is relative to the selected node until the end of the
    match block is reached.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    match_re = re.compile(rf"(out\.open)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.open\(({String.regex}){OPTIONAL_STRING}\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Action for open function."""
        context.writer.open_path(
            self.get_replaced_string(0, context), self.get_repl_opt_string(1, context)
        )
        return PAction.CONTINUE


class Replace(Out):
    """Class for `out.replace` function.
    Like out.create(), but replaces the nodes in the given path if they already exist.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    match_re = re.compile(rf"(out\.replace)\({String.regex}{OPTIONAL_STRING}\)$")
    value_re = re.compile(rf"out\.replace\(({String.regex}){OPTIONAL_STRING}\)")
    value_types = (String, String)

    def execute(self, context: Context) -> PAction:
        """Action for replace function."""
        context.writer.replace_element(
            self.get_replaced_string(0, context), self.get_repl_opt_string(1, context)
        )
        return PAction.CONTINUE


class SetRootName(Out):
    """Class for `out.set_root_name` function.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    max_args = 1

    match_re = re.compile(rf"(out\.set_root_name)\({String.regex}\)$")
    value_re = re.compile(rf"out\.set_root_name\(({String.regex})\)")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Action for set_root_name function."""
        if isinstance(context.writer, Xml):
            context.writer.root_name = self.get_string(0).value
        return PAction.CONTINUE


# Grammars


class GrammarCall(Function):
    """Class for a grammar call.

    :var match_re: Regex matching the function in a string.
    :vartype match_re: Pattern[str]
    :var value_re: Regex matching the arguments in the function match.
    :vartype value_re: Pattern[str]
    """

    min_args = 0
    max_args = 0

    match_re = re.compile(rf"({Varname.regex})\(\)$")
    value_re = re.compile(rf"{Varname.regex}\(\)")
    value_types = (Varname,)

    def execute(self, _) -> None:
        """Action for a grammar call."""
        raise NotImplementedError


FUNCTIONS: list[type[Function]] = [
    Fail,
    Next,
    Return,
    Say,
    Skip,
    Add,
    AddAttribute,
    ClearQueue,
    Create,
    Enter,
    EnqueueAfter,
    EnqueueBefore,
    EnqueueOnAdd,
    Open,
    Replace,
    SetRootName,
    GrammarCall,
]
