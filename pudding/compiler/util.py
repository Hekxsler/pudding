"""Utility functions for compiler."""

from ..tokens.functions.grammar_call import GrammarCall
from ..tokens.functions import *
from ..tokens.token import Token
from ..tokens.statements import *

DEFAULT_TOKENS: tuple[type[Token], ...] = (
    Fail,
    Next,
    Return,
    Say,
    Add,
    AddAttribute,
    ClearQueue,
    Create,
    Enter,
    EnqueueAfter,
    EnqueueBefore,
    EnqueueOnAdd,
    Open,
    Remove,
    Replace,
    SetRootName,
    FromImport,
    Import,
    Define,
    Grammar,
    IMatch,
    Match,
    Skip,
    IWhen,
    When,
    GrammarCall,
)
