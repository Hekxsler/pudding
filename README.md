# Pudding

Pudding converts text files into structured formats such as XML, JSON, or YAML. The syntax and parsing rules are defined using a custom DSL in `.pud` files.

The idea is based on [Gelatin](https://github.com/knipknap/Gelatin).

## Features
- Convert text to XML, JSON, and YAML
- Custom grammar and rule definitions (`.pud` files)
- Modular and extensible design
- Supports complex parsing and output operations

## Usage

### CLI
```bash
pud -s <SYNTAX> -f <FORMAT> <INPUT>
```
- `<SYNTAX>`: Path to the syntax file
- `<FORMAT>`: "xml", "json", or "yaml"
- `<INPUT>`: File to convert

### Python 
Import convert_file, convert_files or convert_string:
```python
from pudding import convert_file, convert_files, convert_string
```
Or directly import the Compiler, Context and Processor classes and create your own functions, statements or Writer.


## Example

See files in tests/data folder.

## License
GPL-3.0-only

## Links
- [GitHub](https://github.com/Hekxsler/pudding)
- [Documentation](http://pudding.readthedocs.io/en/latest/)