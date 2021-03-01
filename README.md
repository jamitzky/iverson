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

`avg = (_@sum) / (_@len)`

where the fork adverb is defined by `(F@fork)(x)==F(x,x)`

|code|meaning|example|
|--|--|--|
|`x >> f`|`f(x)`|`x >> sin_`|
|`f << x`|`f(x)`|`sin_ << x`|
|`f >> g`|`g(f(x))`|`sin_ >> cos_`|
|`f@g`|`f(g(x))`|`sin_@cos_`|
|`f << g`|`f(g(x))`|`sin_ << cos__`|
|`f(g)`|`f(g(x))`|`sin_(cos_)`|
|`f >> op << g`|`op(f(x),g(y))`|` sin_ >>_+_<< cos_`|
|`f + g`|`f(x)+g(x)`|`sin_ + cos_`|
|`f >> op`|`op(f(x),y)`|`sin_ >> _+_`|
|`f(op)`|`f(op(x,y))`|`sin_(_+_)`|
|`op >> f`|`f(op(x,y))`|`_+_ >> sin_`|
|`op << f`|`op(x,f(y))`|`_+_ << sin_`|
|`op@ad`|`ad(op)`|`(_+_)@fork`|
|`f@ad`|`ad(f)`|`sin_@flatmap`|
|`f@N`|`f(f(f...(f(x))))`|`sin_@4`|
|`N>>op`|`op(N,x)`|`2>>_+_`|
|`op<<N`|`op(x,N)`|`_+_<<4`|
|`op(N)`|`op(x,N)`|`(_+_)(3)`|
|`op1+op2`|`op1(x,y)+op2(x,y)`|`(_+_)/(_-_)`|
|`_@lambda`|`fn(lambda)`|`_@math.sin`|
|`_+_`|`x+y`|`_*_`|
|`_+N`|`x+N`|`_*2`|
|`_[i]`|`x[i]`|`_[-1]`|
|`_.func`|`x.func(y)`|`_.split("")`|
|`_(op1, op2, op3)`|`op2(op1(x,y),op3(x,y)`|`_((_+_),(_/_),(_-_))`|
|`op1(op2,op3)`|`op1(op2(x,y),op3(x,y)`|`pow_(_+_,_-_)`|

# We don't need no stinkin for loops

By using the flatmap adverb loops can be completely avoided:

    for i in arr:
        do_something(i)`
    
can now be written as:

`arr >> do_something@flatmap`


# Important J Idioms

## Function concatination

`f@g` denotes the concatination of two functions `f(g(x))` It can be used to generate a new function without writing out an argument. This is called tacit programming. New functions are composed from existing by operators. This is very similar in the programming language Haskell where tacit programming is also a very important tool to generate new functions. In order to accomplish this task in J there exist adverbs and conjunctions. Adverbs are functions with a function as one argument and returning a new function. Conjuctions take 2 functions as arguments and return a new function. They cannot be applied to numers but only on functions and are somehow function-functions or called functors. An example for a adverb is the `map` functor which takes as an argument a function of a scalar variable and is transformed into a function which applies this function to an array or list.

 - predefined adverbs in iverson.py: `fork, flatmap, deepmap, ins, rmap, lmap, rlmap, table, rev, cum, converge, append, tee, rec`
 - predefined conjunctions in iverson.py: `f|g, f^g, f>>g, f<<g, f+g, f-g, f*g, f/g, f%g, f**g, f>g, f<g`

these adverbs and conjunctions can be used to write tacit programs where no explicit variables are stated.



