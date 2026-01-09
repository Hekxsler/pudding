# Pudding syntax

The following functions, statements and types are part of the pudding syntax.
All functions and statements are **one-liners**.

# Value types

## Node
The output generated when running pudding is represented by a tree consisting of nodes.
To select nodes in this string a URL notated string is used.
It consists of the node name, optionally followed by attributes.
Examples:
```
.
element
element?attribute1="foo"
element?attribute1="foo"&attribute2="foo"
```

## Path
A path addresses a node in the tree.
Addressing is relative to the currently selected node.
Path is a string of nodes separated by a slash: `NODE[/NODE[/NODE]]`.
Examples:
```
.
./child
parent/element?attribute="foo"
parent/child1?name="foo"/child?attribute="foobar"
```
## Regular expressions
This type describes a regular expression as used in python, delimited by the character `/`.
Escaping is again done using the backslash character (`\`).
The expression MAY NOT extract any subgroups.
In other words, when using bracket expressions, always use `(?:)`.
Examples:
```
/^(test|foo|bar)$/         # invalid!
/^(?:test|foo|bar)$/       # valid
```
If you are trying to extract a substring, use a match statement with multiple expressions instead.

## String
A string is any series of characters, delimited by the character `'`.
Escaping is done using the backslash character (`\`).
Examples:
```
'test me'
'test \'escaped\' strings'
```

## Varname
Variable names can only contain the following set of characters: `[a-z0-9_]`.


# Statements

## Define
The define statements assigns a value to a variable name.
If the variable has a value already assigned it will be replaced.
This statement can be used anywhere in the code.

Examples:
```
define my_test /(?:foo|bar)/
define my_test2 'foobar'
define my_test3 my_test2
```

## Define
The define statements assigns a value to a variable name.
If the variable has a value already assigned it will be replaced.
This statement can be used anywhere in the code.

Examples:
```
define my_test /(?:foo|bar)/
define my_test2 'foobar'
define my_test3 my_test2
```

## Grammar
Grammar statements define a grammar and behave like define statements.

Example:
```
define nl /[\r\n]+/
define nonl /[^\r\n]+/
define ws /\s+/

grammar default:
    skip ws
    skip nl
    skip '#' nonl nl
```

## Import
Import statements are followed by a single string containing the path to the file.
The file ending of the import path is omitted.
Files must end with `.pud` to be imported.

To import all grammars and variables of another syntax file use:
```
import 'import_me'
```
The input grammar is automatically skipped.

To import only specific variables or grammars use:
```
from 'import_me' import 'string'
from 'import_me' import 'test'
```

All imported grammars and variables are defined at this point.
If you define a grammar or variable with same name as the imported grammar or variable, it will get replaced.

The import statements behave like copying the content of the other file to the position of the import statement.
Importing a grammar or variable will fail if it uses grammars/variables not imported and not defined in the current file.


## Match
Match statements are followed by at least one expression and end with colon (`:`).
Multiple expressions are separated by a space. Examples:
```
define digit /[0-9]/
define number /[0-9]+/

grammar input:
    match 'foobar':
        do.say('Match was: $0!')
    match 'foo' 'bar' /[\r\n]/:
        do.say('Match was: $0!')
    match 'foobar' digit /\s+/ number /[\r\n]/:
        do.say('Matches: $1 and $3')
```
You may also use multiple matches resulting in a logical OR:
```
match 'foo' '[0-9]' /[\r\n]/ | 'bar' /[a-z]/ /[\r\n]/ | 'foobar' /[A-Z]/ /[\r\n]/:
    do.say('Match was: $1!')
```
The expression(s) is matched against the content at the current position.
On a match, the matching string is consumed from the input and the current position in the document is advanced.
Otherwise the next statement in the grammar is executed.

A match statement must be followed by an indented block containing functions.
In this block, the match of each expression can be accessed using `$X`, where X is the position in the list:
```
        $0     $1      $2
match 'foo' '[0-9]' /[\r\n]/:
    do.say('Match was: $1!')
```
```
        $0     $1      $2        $0     $1      $2         $0       $1      $2
match 'foo' '[0-9]' /[\r\n]/ | 'bar' /[a-z]/ /[\r\n]/ | 'foobar' /[A-Z]/ /[\r\n]/:
    do.say('Match was: $1!')
```
`imatch` statements are like match statements, except that matching is case-insensitive.

## Skip
Skip statements are like match statements but without any actions.

Example:
```
define nl /[\r\n]+/
define nonl /[^\r\n]+/
define ws /\s+/

grammar default:
    skip ws
    skip nl
    skip '#' nonl nl
```
`iskip` statements are like skip statements, except that matching is case-insensitive.

## When
When statements are like match statements, with the difference that upon a match, the string is not consumed.
The current position in the content is not advanced.

Example:
```
grammar user:
    match 'Name:' /\s+/ /\S+/ /\n/:
        do.say('Name was: $2!')
    when 'User:':
        do.return()

grammar input:
    match 'User:' /\s+/ /\S+/ /\n/:
        out.enter('user/name', '$2')
        user()
```
`iwhen` statements are like when statements, except that matching is case-insensitive.


# Functions

## Control Functions

```{eval-rst}
.. py:function:: do.fail(message)

   Print a given string to stdout and immediately terminate with an error.

   :param message: Message to print.
   :type message: String


.. py:function:: do.next()

   Immediately execute the next statement or function in the current grammar.


.. py:function:: do.return()

   Immediately leave the current grammar and return to the calling function.
   When used in the input grammar stop parsing.


.. py:function:: do.say(message)

   Print to stdout.

   :param message: Message to print.
   :type message: String
```


## Output Generating Functions

```{eval-rst}
.. py:function:: out.add_attribute(path, name, value)

   Add an attribute to the node in the given path.

   :param path: Path of the node.
   :type path: Path
   :param name: Name of the attribute.
   :type name: String
   :param value: Value of the attribute.
   :type value: String


.. py:function:: out.add(path, text = None)

   Create a node (and attributes) in the given path.
   Nodes will only be created if they do not exist yet.
   If the last node in this path already exists, the text is appended.

   :param path: Path of the node.
   :type path: Path
   :param text: Optional text of the created node.
   :type text: String


.. py:function:: out.clear_queue()

   Removes any items from the queue that were previously added using the out.enqueue_*() functions.


.. py:function:: out.create(path, text = None)

   Create a node (and attributes) in the given path.
   The last node in the path will always be created, so using this function twice with the same path will lead to duplicates.
   The parent nodes will only be created if they do not exist yet.

   :param path: Path of the node.
   :type path: Path
   :param text: Optional text of the created node.
   :type text: String


.. py:function:: out.enter(path, text = None)

   Like out.add(), but also selects the last node in the path.
   The Path of all subsequent function calls are then relative to this node until the next statement or function of the current grammar is reached.

   :param path: Path of the node.
   :type path: Path
   :param text: Optional text of the created node.
   :type text: String


.. py:function:: out.enqueue_after(regex, path, text = None)

   Like out.add(), but is not immediately executed.
   Instead it is executed after the given expression matches the input and the next function was processed.

   :param regex: Pattern to match.
   :type regex: String, Regex or Varname.
   :param path: Path of the node.
   :type path: Path
   :param text: Optional text of the created node.
   :type text: String


.. py:function:: out.enqueue_before(regex, path, text = None)

   Like out.add(), but is not immediately executed.
   Instead it is executed when the given expression matches the input, regardless of the grammar in which the match occurs.

   :param regex: Pattern to match.
   :type regex: String, Regex or Varname.
   :param path: Path of the node.
   :type path: Path
   :param text: Optional text of the created node.
   :type text: String


.. py:function:: out.enqueue_on_add(regex, path, text = None)

   Like out.add(), but is not immediately executed.
   Instead it is executed when the given expression matches the input and a node is added to the output.

   :param regex: Pattern to match.
   :type regex: String, Regex or Varname.
   :param path: Path of the node.
   :type path: Path
   :param text: Optional text of the created node.
   :type text: String


.. py:function:: out.open(path, text = None)

   Like out.create(), but also selects the created node.
   The Path of all subsequent function calls are then relative to this node until the next statement or function of the current grammar is reached.

   :param path: Path of the node.
   :type path: Path
   :param text: Optional text of the created node.
   :type text: String


.. py:function:: out.remove(path)

   Remove a node in the given path.

   :param path: Path of the node.
   :type path: Path


.. py:function:: out.replace(path, text)

   Replace the text of a node in the given path.

   :param path: Path of the node.
   :type path: Path
   :param text: New text of the node.
   :type text: String


.. py:function:: out.set_root_name(name)

   Specifies the tag of the root node, if the output is XML.
   Has no effect on JSON and YAML output.

   :param name: Name of the root node.
   :type name: String
```
