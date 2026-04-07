## Introduction

Vexo is an interpreted programming language with simple syntax, designed for learning programming basics and quickly creating small scripts. The language combines understandable constructs from natural language with powerful built-in functions.

### Key Features

- Simple and intuitive syntax
- Dynamic typing
- Floating-point number support
- Built-in mathematical functions
- Type conversion
- Data input/output

---

## Data Types

### Numbers (Number)
Integers.

```vexo
make var x = 42
make var y = -7
```

### Floating-point numbers (Float)
Real numbers.

```vexo
make var pi = 3.14159
make var negative = -0.5
```

### Strings (String)
Text data enclosed in double quotes.

```vexo
make var name = "Vexo"
make var message = "Hello, World!"
```

### Boolean type (Logic)
Boolean values `true` or `false`.

```vexo
make var isReady = true
make var isComplete = false
```

---

## Variables

### Declaring Variables
The `make var` keyword is used to create a variable:

```vexo
make var age = 25
make var name = "Alice"
make var isValid = true
```

### Using Variables
```vexo
make var x = 10
make var y = x + 5
say(y)  # Outputs: 15
```

---

## Operators

### Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition and concatenation | `5 + 3`, `"Hello" + "World"` |
| `-` | Subtraction | `10 - 4` |
| `*` | Multiplication | `6 * 7` |
| `/` | Division | `15 / 3` |

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal to | `x == y` |
| `!=` | Not equal to | `x != y` |
| `<` | Less than | `x < y` |
| `>` | Greater than | `x > y` |
| `<=` | Less than or equal to | `x <= y` |
| `>=` | Greater than or equal to | `x >= y` |

### Logical Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Logical AND | `x > 0 and y < 10` |
| `or` | Logical OR | `x == 5 or y == 5` |
| `not` | Logical NOT | `not isReady` |

---

## Output Functions

### say()
Outputs a value with an automatic newline.

```vexo
say("Hello, World!")  # Hello, World!
say(42)               # 42
say(true)             # true

make var name = "Vexo"
say("Welcome to " + name)  # Welcome to Vexo
```

### stick()
Outputs a value without a newline (concatenates output).

```vexo
stick("Hello")
stick(" ")
stick("World")  # Hello World
```

---

## Input Function

### ask()
Prompts the user for data input. Returns the entered value with automatic type detection.

```vexo
make var name = ask("Enter your name:")
say("Hello, " + name)

make var age = ask("Enter your age:")
say(age + 10)  # If 25 is entered, outputs 35

make var answer = ask("Do you like Vexo? (true/false):")
if answer == true {
    say("Great!")
}
```

**Automatic type detection:**
- `true`/`false` → boolean type
- Numbers without a decimal point → integer
- Numbers with a decimal point → floating-point number
- Everything else → string

---

## Type Conversion

### number()
Converts a value to an integer.

```vexo
make var a = number("123")    # 123
make var b = number(45.67)    # 45
make var c = number(true)     # 1
make var d = number(false)    # 0
```

### float()
Converts a value to a floating-point number.

```vexo
make var a = float("3.14")    # 3.14
make var b = float(42)        # 42.0
make var c = float(true)      # 1.0
```

### string()
Converts a value to a string.

```vexo
make var a = string(123)      # "123"
make var b = string(3.14)     # "3.14"
make var c = string(true)     # "true"
```

### logic()
Converts a value to a boolean type.

```vexo
make var a = logic(1)         # true
make var b = logic(0)         # false
make var c = logic("hello")   # true
make var d = logic("")        # false
```

**Rules for converting to boolean type:**
- Numbers: `0` → `false`, everything else → `true`
- Strings: empty string → `false`, non-empty → `true`
- Boolean values: remain unchanged

---

## Mathematical Functions

### math root()
Calculates the square root of a number.

```vexo
make var result = math root(16)   # 4.0
make var value = math root(2)     # 1.4142135623730951
```

### math roundUp()
Rounds a number to the nearest integer (mathematical rounding).

```vexo
make var a = math roundUp(3.2)    # 3
make var b = math roundUp(3.7)    # 4
make var c = math roundUp(4.5)    # 5
```

---

## Syntax Rules

1. Each command can be written on one line, preferably using ";": `say("Hello,"); say("World!")`
2. To write a comment, first type "//", then the text; in the editor, this text will turn dark green

---

## Conclusion

Vexo is a simple and understandable programming language, ideal for beginners. Thanks to its intuitive syntax and built-in functions, you can quickly learn programming basics and create your first projects.
