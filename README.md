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


The data flow operators show their full potential when they are combined with dyadic functions. e.g. `Div(x,y)==x/y` and the fork adverb

`Avg = Sum >> Div << Len | fork`

where the fork adverb is defined by `(F@fork)(x)==F(x,x)`

|code|meaning|
|--|--|
|`x >> f`|`f(x)`|
|`f << x`|`f(x)`|
|`f >> g`|`g(f(x))`|
|`f@g`|`f(g(x))`|
|`f << g`|`f(g(x))`|
|`f(g)`|`f(g(x))`|
|`f >> op << g`|`op(f(x),g(y))`|
|`f + g`|`f(x)+g(x)`|
|`f >> op`|`op(f(x),y)`|
|`f(op)`|`f(op(x,y))`|
|`op >> f`|`f(op(x,y))`|
|`op << f`|`op(x,f(y))`|
|`op@ad`|`ad(op)`|
|`f@ad`|`ad(f)`|
|`f@N`|`f(f(f...(f(x))))`|
|`N>>op`|`op(N,x)`|
|`op<<N`|`op(x,N)`|
|`op(N)`|`op(x,N)`|
|`op1+op2`|`op1(x,y)+op2(x,y)`|
|`_@lambda`|`fn(lambda)`|
|`_+_`|`x+y`|
|`_+N`|`x+N`|
|`_[i]`|`x[i]`|
|`_.func`|`x.func(y)`|
|`_(op1, op2, op3)`|`op2(op1(x,y),op3(x,y)`|

# We don't need no stinkin for loops

By using the flatmap adverb loops can be completely avoided:

    for i in arr:
        do_something(i)`
    
can now be written as:

`arr >> do_something@flatmap`



