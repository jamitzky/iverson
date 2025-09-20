# Iverson

python extension which mimics J syntax

# General

## Design Philosophy

The code implements a domain-specific language for functional programming where:
1. Functions are first-class citizens
2. Composition is emphasized over explicit variable binding
3. Mathematical notation is preserved through operator overloading
4. Higher-order functions and adverbs provide powerful abstractions

This creates a Python implementation of a DSL with concise syntax for expressing complex functional transformations, particularly useful for mathematical and data processing operations. The system is inspired by languages like J, K and APL, which emphasize mathematical notation and functional programming concepts. Let me break down its use cases and examples:

## Main Use Cases

### 1. **Point-free Programming**
Write functions without explicitly naming parameters, similar to APL/J's tacit programming style.

### 2. **Function Composition and Operators**
Chain operations and create new functions through operator overloading.

### 3. **Higher-order Functions**
Support for adverbs (functions that transform other functions) and conjunctions.

## Key Features

### Point-Free Programming
The system allows writing functions without explicit variable names:
```python
# Instead of: lambda x: x**2
sqr = _**2

# Instead of: lambda x, y: x + y  
add = _ + _

# Instead of: lambda x: x + 1
inc = _ + 1
```

### Function Composition
- `f >> g` means "apply f, then g" (right composition)
- `f << g` means "apply g, then f" (left composition)
- `f @ g` can apply a function g times to f

### Higher-Order Functions (Adverbs)
- `fork`: Creates a function that applies the same argument twice
- `flatmap`: Maps a function over a list and flattens results
- `ins`/`insert`: Reduces a list with an operator
- `rmap`/`lmap`: Maps functions over lists in different ways

### Examples of Usage
```python
# Create functions
sqr = fn("x**2")
sqrt = fn(lambda x: x**0.5)

# Function composition
composition = sqr >> sqrt  # sqrt(sqr(x))

# Point-free operators
add = _ + _          # x + y
inc = _ + 1          # x + 1
square = _**2        # x**2

# Higher-order operations
double_map = flatmap(lambda x: [x, x])  # Maps each element to [x, x]

# Complex expressions
primes = R >> fork(_unless_ << fork(ε << table(X*Y)@fork@R)@µ)
```
# We don't need no stinkin for loops

By using the flatmap adverb loops can be completely avoided:

```python
for i in arr:
    do_something(i)`
```

can now be written as:

`arr >> do_something@flatmap`


It defines three different function classes (two verbs and one adverb):

*   Single argument functions (aka monads) `fn(lambda x: f(x))`
*   Dual argument functions (aka infix operators aka dyads) `op(lambda x,y: g(x,y))`
*   Functors (aka functions on functions aka adverbs) for monads and dyads `ad(lambda f: fn(g(f)))`

Six overloaded operators which operate on the above classes:

*   Data flow operators >> and \<\< which specify the data flow from one verb to another `(f << g)(x) == f(g(x))` and `(f >> g)(x) == g(f(x))`
*   Inline function decorator which modifies a function in place: `(f@g)(x) == (g(f))(x)`
*   Function power operator for repeated application of a function: `(f^3)(x) == f(f(f(x)))`

The data flow operators show their full potential when they are combined with dyadic functions. e.g. `Div(x,y)==x/y` and the fork adverb

`avg = (_@sum) / (_@len)`

where the fork adverb is defined by `(F@fork)(x)==F(x,x)`

| code | meaning | example |
| --- | --- | --- |
| `x >> f` | `f(x)` | `x >> sin_` |
| `f << x` | `f(x)` | `sin_ << x` |
| `f >> g` | `g(f(x))` | `sin_ >> cos_` |
| `f@g` | `f(g(x))` | `sin_@cos_` |
| `f << g` | `f(g(x))` | `sin_ << cos__` |
| `f(g)` | `f(g(x))` | `sin_(cos_)` |
| `f >> op << g` | `op(f(x),g(y))` | `sin_ >>_+_<< cos_` |
| `f + g` | `f(x)+g(x)` | `sin_ + cos_` |
| `f >> op` | `op(f(x),y)` | `sin_ >> _+_` |
| `f(op)` | `f(op(x,y))` | `sin_(_+_)` |
| `op >> f` | `f(op(x,y))` | `_+_ >> sin_` |
| `op << f` | `op(x,f(y))` | `_+_ << sin_` |
| `op@ad` | `ad(op)` | `(_+_)@fork` |
| `f@ad` | `ad(f)` | `sin_@flatmap` |
| `f@N` | `f(f(f...(f(x))))` | `sin_@4` |
| `N>>op` | `op(N,x)` | `2>>_+_` |
| `op<<N` | `op(x,N)` | `_+_<<4` |
| `op(N)` | `op(x,N)` | `(_+_)(3)` |
| `op1+op2` | `op1(x,y)+op2(x,y)` | `(_+_)/(_-_)` |
| `_@lambda` | `fn(lambda)` | `_@math.sin` |
| `_+_` | `x+y` | `_*_` |
| `_+N` | `x+N` | `_*2` |
| `_[i]` | `x[i]` | `_[-1]` |
| `_.func` | `x.func(y)` | `_.split("")` |
| `_(op1, op2, op3)` | `op2(op1(x,y),op3(x,y)` | `_((_+_),(_/_),(_-_))` |
| `op1(op2,op3)` | `op1(op2(x,y),op3(x,y)` | `pow_(_+_,_-_)` |




This code defines a functional programming framework in Python that allows for point-free (tacit) programming using custom classes and operator overloading. Here's a breakdown of the main components:

## Core Classes

### `fn` (Function Class)
- Represents mathematical functions
- Can be created from strings like `"x**2"` or lambda functions
- Supports function composition and arithmetic operations
- Implements overloaded operators for function manipulation:
  - `|` for right composition (`f >> g`)
  - `^` for left composition (`f << g`)  
  - `@` for function decorators and repeated application
  - `>>` and `<<` for function composition
  - Arithmetic operators (`+`, `-`, `*`, `/`, `**`) for function arithmetic

### `op` (Operator Class)
- Represents binary operators
- Can be created from strings like `"x+y"` or lambda functions
- Supports operator composition and arithmetic operations
- Implements operators for currying and function application

### `ad` (Adverb Class) 
- Represents adverbs (functions that take functions and return functions)
- Examples include `fork`, `flatmap`, `ins` (insert/reduce), `rmap`, `lmap`, etc.
- Provides higher-order functionality for manipulating functions

### `uscore` (Underscore Class)
- Represents the placeholder `_` for point-free notation
- Enables syntax like `(_+_)` for binary operations and `(_+2)` for unary operations
- Supports currying and operator creation




## Key Components

### **`fn` class** - Function objects
```python
# Create functions from strings or lambdas
sqr = fn("x**2")
sqrt = fn(lambda x: x**0.5)

# Function composition with >> and <<
result = sqr >> sqrt  # sqrt(sqr(x))
```

### **`op` class** - Operator objects (binary functions)
```python
# Binary operators
add = op("x+y")
mul = op(lambda x,y: x*y)

# Operators can be curried
add2 = add(2)  # x + 2
```

### **`uscore` class** - `_` placeholder
```python
# `_` represents "any argument"
add = _ + _        # equivalent to op("x+y")
add2 = _ + 2       # equivalent to op("x+2")
```

# Important J Idioms

## Function concatination

`f@g` denotes the concatination of two functions `f(g(x))` It can be used to generate a new function without writing out an argument. This is called tacit programming. New functions are composed from existing by operators. This is very similar in the programming language Haskell where tacit programming is also a very important tool to generate new functions. In order to accomplish this task in J there exist adverbs and conjunctions. Adverbs are functions with a function as one argument and returning a new function. Conjuctions take 2 functions as arguments and return a new function. They cannot be applied to numers but only on functions and are somehow function-functions or called functors. An example for a adverb is the `map` functor which takes as an argument a function of a scalar variable and is transformed into a function which applies this function to an array or list.

*   predefined adverbs in iverson.py: `fork, flatmap, deepmap, ins, rmap, lmap, rlmap, table, rev, cum, converge, append, tee, rec`
*   predefined conjunctions in iverson.py: `f|g, f^g, f>>g, f<<g, f+g, f-g, f*g, f/g, f%g, f**g, f>g, f<g`

these adverbs and conjunctions can be used to write tacit programs where no explicit variables are needed.

Furthermore the functions to which these operators are applied to do not have to be only functions of a single variable (aka monads) but can also be functions of 2 variables (aka dyads).  
For example the function to sum up an array of numbers can be defined by: `sum = (_+_)@ins` which means `insert` the function `(_+_)` into the array between the numbers and add all the elements.

By using the function `one=fn(lambda x:1)` we can then define a length function for arrays by using the `flatmap` adverb by `length = sum@(one@flatmap)` and furthermore a function `mean = sum/length` which computes the sum and the length of an array and then divides the two values by each other giving the mean of the array.

## APL/J Relationship

This code directly mimics APL/J concepts:

### **APL/J Features Implemented:**
1. **Monadic and Dyadic Operators** - `fn` and `op` classes
2. **Function Composition** - `>>` (right compose) and `<<` (left compose)
3. **Adverbs** - `fork`, `flatmap`, `ins`, etc.
4. **Tacit Programming** - Point-free style using `_` and operators
5. **Array Operations** - `table`, `rmap`, `lmap`, etc.

### **Example Translation:**

**J Language:**
```j
f =: +/ @: *
g =: f @: i.
```

**Python Equivalent:**
```python
f = sum_ @ ins(_*_ )  # sum_ is insert operator
g = f @ range_        # apply to range
```

## Practical Examples

### **Prime Number Generation:**
```python
# Find primes < 100
primes = R >> fork(_unless_ << fork(ε << table(X*Y)@fork@R)@µ)
```

### **Fibonacci Sequence:**
```python
# Generate Fibonacci numbers
Fib = append(_[-1] + _[-2])
result = [1,1] >> Fib@10  # First 10 Fibonacci numbers
```

### **Monte Carlo Pi Calculation:**
```python
# Estimate pi using random sampling
pi_estimate = 1000000 >> ψ(ψ(χ>>rlµ(_**2>>_+_<<_**2>>_**0.5>>(_<1))<<χ) >> Σ*4 >> _/_)
```

### **List Transformations:**
```python
# Map square to list
squares = sqr @ [1,2,3,4]  # [1,4,9,16]

# Apply function 5 times
result = f@5(x)  # f(f(f(f(f(x)))))
```

## Key Features

1. **Operator Overloading**: Uses `>>`, `<<`, `@`, `|`, `^` for functional composition
2. **Adverbs**: Higher-order functions that modify functions (`fork`, `flatmap`, `ins`)
3. **Currying**: Operators can be partially applied
4. **Point-free Style**: Write functions without explicit variable names
5. **Tacit Programming**: Express computations in terms of function composition

## Language Comparison

| APL/J | Python (this implementation) | Purpose |
|-------|-----------------------------|---------|
| `+/` | `sum_` | Sum reduction |
| `f g h` | `f >> g >> h` | Function composition |
| `f@` | `f@` | Adverb application |
| `_` | `_` | Placeholder for arguments |
| `∘` | `>>` | Function composition |
| `⍥` | `@` | Power/iteration |

This implementation essentially brings the elegant mathematical and functional programming concepts of APL and J into Python's syntax, enabling concise, expressive code for data transformations and mathematical operations.
