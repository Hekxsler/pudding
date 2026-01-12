# Quick Start

## Converting a file
Suppose you want to convert the following text file to XML:
```
User
----
Name: John, Lastname: Doe
Office: 1st Ave
Birth date: 1978-01-01

User
----
Name: Jane, Lastname: Foo
Office: 2nd Ave
Birth date: 1970-01-01
```

The following syntax file does the job:
```
# Define commonly used data types. This is optional, but
# makes your life a litte easier by allowing to reuse regular
# expressions in the grammar.
define nl /[\r\n]/
define ws /\s+/
define fieldname /[\w ]+/
define value /[^\r\n,]+/
define field_end /[\r\n,] */

grammar user:
    match 'Name:' ws value field_end:
        out.add_attribute('.', 'firstname', '$2')
    match 'Lastname:' ws value field_end:
        out.add_attribute('.', 'lastname', '$2')
    match fieldname ':' ws value field_end:
        out.add('$0', '$3')
    match nl:
        do.return()

# The grammar named "input" is the entry point for the converter.
grammar input:
    match 'User' nl '----' nl:
        out.open('user')
        user()
```

Execution steps explained:
1. The grammar `input` is the entry point for the processor
2. Statements in each grammar are executed sequentially. If a match is found, the indented functions of this statement are executed and the grammar restarts at the top of the grammar. Otherwise the next statement or function will be executed.
3. `out.add('$0', '$3')` creates a node if it does not yet exist. The name of the node is the value of the first matched expression (the fieldname, in this case). The data of the node is the value of the fourth matched field.
4. `out.open('user')` creates a node with the tag "user" and selects it. Meaning all following function in this statement generate output relative to this node.
5. `user()` calls the grammar named "user".
6. If the end of a grammar is reached before the end of the input document was reached, an error is raised.


This produces the following output in XML:
```xml
<xml>
  <user lastname="Doe" firstname="John">
    <office>1st Ave</office>
    <birth-date>1978-01-01</birth-date>
  </user>
  <user lastname="Foo" firstname="Jane">
    <office>2nd Ave</office>
    <birth-date>1970-01-01</birth-date>
  </user>
</xml>
```


## Using pudding as a python module

Pudding also provides a Python API for transforming files and strings:
```python
from pudding import convert_file, convert_files, convert_string
``` 
See the [API Reference](./api.md#core-module) for more details.

