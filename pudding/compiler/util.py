"""Utility functions for compiler."""

from ..tokens import statements as stmt
from ..tokens.functions import do, out
from ..tokens.functions.grammar_call import GrammarCall
from ..tokens.token import Token

DEFAULT_TOKENS: tuple[type[Token], ...] = (
    do.Fail,
    do.Next,
    do.Return,
    do.Say,
    out.Add,
    out.AddAttribute,
    out.ClearQueue,
    out.Create,
    out.Enter,
    out.EnqueueAfter,
    out.EnqueueBefore,
    out.EnqueueOnAdd,
    out.Open,
    out.Remove,
    out.Replace,
    out.SetRootName,
    stmt.Define,
    stmt.FromImport,
    stmt.Import,
    stmt.Grammar,
    stmt.IMatch,
    stmt.Match,
    stmt.Skip,
    stmt.IWhen,
    stmt.When,
    GrammarCall,
)
