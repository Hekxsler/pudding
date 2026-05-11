# Customizing pudding

Pudding is built highly customizable and modular.
You can customize any part to get the behaviour and output you want.

Most likely you want a custom writer class to get a different output format.
But you can also write your own statements, functions or even compiler.

On this page there is a overview of how pudding works internally and an example of how to create a custom function. Of course pudding can do much more, but this would be too much to write down :)

## How pudding works

### 1. Compiling the syntax

First of all, you need the compiled syntax for the processor.
```python
from pudding.compiler import Compiler

syntax = Compiler().compile_file(syntax_file)
# or
syntax = Compiler().compile(syntax_string)
```
If no arguments are given the compiler uses the default tokens.
You can limit or extend the allowed tokens by giving a list of tokens when initializing the compiler class.
See [Compiler](./api.md#compiler-module) in the API Reference.


### 2. Creating the context

The processor also needs a context object containing a reader class with the input and writer class for the wanted output format.
```python
from pudding.processor.context import Context
from pudding.reader import Reader
from pudding.writer import Xml

reader = Reader(content)
writer = Xml(output_file, encoding=encoding)
context = Context(reader, writer)
```
Both classes Reader and Writer can be customized by inheriting the base class and giving them to the context at this point.
```{admonition} Tip
View the [Writer module](./api.md#writer-module) in the API Reference first and decide which class suits you best as a base class.
```


### 3. Converting and writing the output

Now we can combine everything and initialize the processor class with the context and syntax.
```python
from pudding.processor.processor import Processor

writer = Processor(context, syntax).convert()
writer.write_output()
```
Running `.convert()` starts the conversion of the input.
If you do not use a writer that writes directly into files like SliXml, call `.write_output()` to write to a file.
Otherwise you can use `.generate_output()` to receive the converted input as a string.


## Adding a simple custom function
Here is an example of a custom function:
```python
import re
import requests

from pudding.datatypes import String
from pudding.processor import PAction
from pudding.processor.context import Context
from pudding.tokens.functions.function import Function

class SendRequest(Function):
    """Class for `send` function.

    Send a GET request to the provided url.
    """
    min_args = 1
    max_args = 1

    match_re = re.compile(r"(custom\.send_request)\((.*)\)$")
    value_types = (String,)

    def execute(self, context: Context) -> PAction:
        """Send a GET request.

        :param context: Current context object.
        :returns: Returns PAction.CONTINUE for processor class.
        """
        url = context.replace_string_vars(self.get_string(0))
        print(requests.get(url))
        return PAction.CONTINUE

```

### Naming your function
Function names should follow the existing scheme, e.g. `custom.function()`. Otherwise custom functions with no arguments will prevent grammars with the same name from being called.
It should also not be overriding any other function names.

### Class attributes
- min_args: Integer defining the minimum amount of arguments.
- max_args: Integer defining the maximum amount of arguments.
- match_re: Compiled regular expression matching the function name and arguments. It must contain two groups where the first group matches the function name and the second matching the values including any delimiters (commas, spaces, etc.).
- value_types: Tuple of datatypes in order of the arguments. Available are Regex, String and Varname. See [Value types](./syntax.md#value-types)

### Execute function
This function is called when the processor calls your function.
It takes the context object and returns a PAction (processor action).

To get mandatory string values use the get_string method. It raises a TypeError if the value at the given index is not a string. Otherwise you need to use get_values.

Using the context object you can, for example, replace the variables in the string with matched values.

Finally return a PAction, telling the processor what to do next.
Unless you want a specific behaviour, I recommend keeping this to `PAction.CONTINUE`.

### Adding it to the compiler
As described above you need give all occuring tokens to the compiler.
```python
from pudding.compiler import Compiler
from pudding.compiler.util import DEFAULT_TOKENS

tokens = DEFAULT_TOKENS + (SendRequest,)
compiler = Compiler(tokens)
...
```
From here you can follow the steps 2 and 3 to convert your content.
