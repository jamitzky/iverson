# Iverson
python extension which mimics J syntax
The package defines 3 function classes: function (single argument), operator (dual arguments) and adverbs (functions as arguments) and  5 operators for these function classes (<<, >>, |, & and ^)

# General
This python package defines a DSL for functional programming in the style of the array languages APL, J and K. 

It defines three different function classes:
 - Single argument functions (aka monads) *fn(x)*
 - Dual argument functions (aka infix operators aka dyads) *op(x,y)*
 - Functors (aka functions on functions aka adverbs) for monads and dyads *ad(f)*
 
Six overloaded operators which operate on the above classes:
 -  Data flow operators >> and << which specify the data flow from one verb to another *(f << g)(x) == f(g(x))* and *(f >> g)(x) == g(f(x))*
 - inline decorator which modify a function in place: *(f@g)(x) == (g(f))(x)* 
 - function power operator for repeated application of a function: *(f^3)(x) == f(f(f(x)))*
 - Syntactic sugar for the above operators: *(f << g | h)(x) == ((f<<g)@h)(x)*
 
