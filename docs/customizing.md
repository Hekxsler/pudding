# Customizing pudding

Pudding is built highly customizable and modular.
You can customize any part to get the behaviour and output you want.

The most likely use is a custom writer class to get a different output format.
But you can also write your own statements, functions or even compiler.

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
