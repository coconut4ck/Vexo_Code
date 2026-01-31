# Libraries
Libraries are a folder with the name of the library itself, and it should always contain lexer files.py and parser.py

# Create your own library
## To create your own library, you need to know a few things:
#### -Folder name -> Library name
#### -There must be lexer scripts in the lexer.py and parser.py

## Creating in parser.py main class:
```python
class Name:
  all functions below
```
## Now in lexer.py we write commands:
```python
def command(arguments(if needed for the command)):
  return parser_instance.parameter command(the command must match a function from the class)
#parser_instance < is a global variable that can be used to connect parser.py
#you should also always set return so that when the function is activated, it outputs something.
```
## After these actions in parser.py we start writing the command:
```python
class Name:
  def ragse_command(arguments (if needed for the command)):
    ...code...
    return Here we write what it should send when writing this command
```
## And at this stage everything ends!

# How do I use commands from the library?
## You need to open the settings of the Rix Script editor and specify the path to the folder with all the libraries
## We need to write this command at the beginning of the code:
```rix script
#lib -> Name of the library(folder)
```
