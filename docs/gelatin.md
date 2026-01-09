# Changes from Gelatin

Pudding is not based on Gelatin and therefore does things differently.

## Multiline regular expressions
Things like these are currently no longer possible:
```
match 'foo' '[0-9]' /[\r\n]/
    | 'bar' /[a-z]/ /[\r\n]/
    | 'foobar' /[A-Z]/ /[\r\n]/:
    do.say('Match was: $1!')
```
Solutions are changing it to a single line:
```
match 'foo' '[0-9]' /[\r\n]/ | 'bar' /[a-z]/ /[\r\n]/ | 'foobar' /[A-Z]/ /[\r\n]/:
    do.say('Match was: $1!')
```
Or splitting it up in seperate statements:
```
match 'foo' '[0-9]' /[\r\n]/:
    do.say('Match was: $1!')
match 'bar' /[a-z]/ /[\r\n]/:
    do.say('Match was: $1!')
match 'foobar' /[A-Z]/ /[\r\n]/:
    do.say('Match was: $1!')
```

## Removal of do.skip() / skip multiple expressions

The function `do.skip()` has been removed, because `skip` now supports multiple expressions.
For example, this
```
match 'foo' /[0-9]/:
    do.skip()
```
becomes this:
```
skip 'foo' /[0-9]/
```

## New in pudding

### Imports

Pudding allows you to import grammars and variables from other files.
See the [syntax documentation](./syntax.md#import) for more details on how to use it.


### Case insensitive when- and skip-statement

Behaviour is equal to the regular `when` and `skip` statement.
The statements for the case insensitive variant are `iwhen` and `iskip`.


### out.remove()

New function to remove a previously created node.
See the [syntax documentation](./syntax.md#out.remove) for more details on how to use it.
