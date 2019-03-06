# Iverson
python extension which mimics J syntax

# General
This python package defines a DSL for functional programming in the style of the array languages APL, J and K. 

It defines three different function classes (two verbs and one adverb):
 - Single argument functions (aka monads) `fn(lambda x: f(x))`
 - Dual argument functions (aka infix operators aka dyads) `op(lambda x,y: g(x,y))`
 - Functors (aka functions on functions aka adverbs) for monads and dyads `ad(lambda f: fn(g(f)))`


Six overloaded operators which operate on the above classes:
 -  Data flow operators >> and << which specify the data flow from one verb to another `(f << g)(x) == f(g(x))` and `(f >> g)(x) == g(f(x))`
 - Inline function decorator which modifies a function in place: `(f@g)(x) == (g(f))(x)` 
 - Function power operator for repeated application of a function: `(f^3)(x) == f(f(f(x)))`
 - Syntactic sugar for the above operators: `(f << g | h)(x) == ((f<<g)@h)(x)`
 - `([f,g]&h)(x,y) == if h(y): g(x) else: f(x)` which is the same as the ternary operator `h(y)?g(x):f(x)`
The data flow operators show their full potential when they are combined with dyadic functions. e.g. `Div(x,y)==x/y` and the fork adverb
`Avg = Sum >> Div << Len | fork`
where the fork adverb is defined by `(F@fork)(x)==F(x,x)`
