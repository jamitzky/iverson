#
# (c) Ferdinand Jamitzky 2019
#

class fn:
    __array_priority__=2
    def __init__(self, function):
        if type(function)==str:
            self.function=eval("lambda x:"+function)
        else:
            self.function = function
    def __ror__(self, other):
        print("ror")
    def __or__(self, other):
        return other.function(self)
    def __matmul__(self, other):
        #print("matmul",other)
        if type(other)==ad:
            return other.function(self)
        elif type(other)==int:
            if other==1:
                return self
            elif other==0:
                return fn(lambda x:x)
            else:
                return self << self@(other-1)
        elif type(other)==fn:
            @op
            def if_helper(x,y):
                if other.function(y):
                    return self.function(x)
                else:
                    return x
            return if_helper
    def __rrshift__(self, other):
        #print("fn other>>self")
        if type(other)==fn:
            return fn(lambda x,self=self,other=other: self.function(other.function(x)))
        elif type(other)==op:
            return op(lambda x,y,self=self,other=other: self.function(other.function(x,y)))
        else:
            return self(other)
    def __rshift__(self,other):
        if type(other)==fn:
            return fn(lambda x,self=self,other=other: other.function(self.function(x)))
        elif type(other)==op:
            return op(lambda x,y,self=self,other=other: other.function(self.function(x),y))
        else:
            return self(other)
    def __lshift__(self, other):
        #print("fn self<<other")
        if type(other)==fn:
            return fn(lambda x,self=self,other=other: self.function(other.function(x)))
        else:
            return self(other)
    def __call__(self, value):
        #print(value)
        return self.function(value)
    def __add__(self,other):
        "f+g (x) = f(x)+g(x)"
        if type(other)==fn:
            return fn(lambda x:self(x)+other(x))
        else:
            return fn(lambda x:self(x)+other)
    def __sub__(self,other):
        if type(other)==fn:
            return fn(lambda x:self(x)-other(x))
        else:
            return fn(lambda x:self(x)-other)
    def __mul__(self,other):
        if type(other)==fn:
            return fn(lambda x:self(x)*other(x))
        else:
            return fn(lambda x:self(x)*other)
    def __truediv__(self,other):
        if type(other)==fn:
            return fn(lambda x:self(x)/other(x))
        else:
            return fn(lambda x:self(x)/other)
    def __pow__(self,other):
        if type(other)==fn:
            return fn(lambda x:self(x)**other(x))
        else:
            return fn(lambda x:self(x)**other)

class op:
    __array_priority__=2    
    def __init__(self, function):
        #print(function)
        if type(function)==str:
            #print("string")
            self.function=eval("lambda x,y:"+function)
        else:
            self.function = function
    def __ror__(self, other):
        print("ror")
    def __or__(self, other):
        #print("self|ad")
        return other.function(self)
    def __matmul__(self, other):
        #print("self@ad")
        return other.function(self)
    def __rrshift__(self, other):
        #print("op other>>self")
        if type(other)==fn:
            return op(lambda x,y,self=self,other=other:self.function(other.function(x),y))
        else:
            return fn(lambda x,self=self,other=other:self.function(other,x))
    def __lshift__(self, other):
        #print("op self<<other")
        if type(other)==fn:
            return op(lambda x,y,self=self,other=other:self.function(x,other.function(y)))
        else:
            return fn(lambda x,self=self,other=other:self.function(x,other))
    def __call__(self, value1, value2=None):
        #print(" op(x,y) and op(x)")
        if value2==None:
            return fn(lambda x,self=self: self.function(value1,x))
        else:
            return self.function(value1, value2)
class ad:
    __array_priority__=2    
    def __init__(self, function):
        self.function = function
    def __call__(self,verb):
        return self.function(verb)

# underscore definition
import operator
class uscore:
    __array_priority__=2
    def __init__(self):
        pass
    def __add__(self,other):
        if type(other)==uscore:
            return op(operator.__add__)
        else:
            return fn(lambda x,other=other:operator.__add__(x,other))
    def __radd__(self,other):
        return fn(lambda x,other=other:operator.__add__(other,x))
    def __sub__(self,other):
        if type(other)==uscore:
            return op(operator.__sub__)
        else:
            return fn(lambda x,other=other:operator.__sub__(x,other))
    def __mul__(self,other):
        if type(other)==uscore:
            return op(operator.__mul__)
        else:
            return fn(lambda x,other=other:operator.__mul__(x,other))
    def __truediv__(self,other):
        if type(other)==uscore:
            return op(operator.__truediv__)
        else:
            return fn(lambda x,other=other:operator.__truediv__(x,other))
    def __pow__(self,other):
        if type(other)==uscore:
            return op(operator.__pow__)
        else:
            return fn(lambda x,other=other:operator.__pow__(x,other))
    def __gt__(self,other):
        if type(other)==uscore:
            return op(operator.__gt__)
        else:
            return fn(lambda x,other=other:operator.__gt__(x,other))
    def __lt__(self,other):
        if type(other)==uscore:
            return op(operator.__lt__)
        else:
            return fn(lambda x,other=other:operator.__lt__(x,other))
    def __eq__(self,other):
        if type(other)==uscore:
            return op(operator.__eq__)
        else:
            return fn(lambda x,other=other:operator.__eq__(x,other))
    def __in__(self,other):
        "fixme"
        if type(other)==uscore:
            return op(operator.__in__)
        else:
            return fn(lambda x,other=other:operator.__in__(x,other))
    def __getitem__(self,other):
        if type(other)==uscore:
            return op(operator.__getitem__)
        else:
            return fn(lambda x,other=other:operator.__getitem__(x,other))
    def __getattr__(self,other):
        #out=getattr(x,other)
        #if type(out) is type(any):
        return op(lambda x,y,other=other:getattr(y,other)(x))
    def __call__(self,f1,f2,f3):
        return op(lambda x,y,f1=f1,f2=f2,f3=f3: f2(f1(x,y),f3(x,y)))

_=uscore()


# adverbs definition
fork=ad(lambda f: fn(lambda x,f=f:f.function(x,x)))
flatmap=ad(lambda f: fn(lambda x,f=f: [f.function(i) for i in x]))
deepmap=ad(lambda f:f)

@ad
def ins(f):
    "insert operator into list aka reduce function"
    @fn
    def insert_helper(x):
        s0=f(x[0],x[1])
        for xx in x[2:]:
            s0=f(s0,xx)
        return s0
    return insert_helper

rmap=ad(lambda f: op(lambda x,y,f=f: [f.function(x,i) for i in y]))
lmap=ad(lambda f: op(lambda x,y,f=f: [f.function(i,y) for i in x]))
rlmap=ad(lambda f: op(lambda x,y,f=f: [f.function(x[i],y[i]) for i in range(len(x))])) # elementwise
table=ad(lambda f: op(lambda x,y,f=f: [f.function(i,j) for i in x for j in y]))
rev=ad(lambda f: op(lambda x,y,f=f:f.function(y,x)))

@ad
def cum(f):
    "cumulative insert"
    @fn
    def cum_helper(x):
        s0=f(x[0],x[1])
        outs=[s0]
        for xx in x[2:]:
            s0=f(s0,xx)
            outs.append(s0)
        return outs
    return cum_helper
@ad
def converge(f):
    "apply until no more changes"
    @fn
    def converge_helper(x):
        out=f(x)
        old=x
        while old!=out:
            old=out
            out=f(out)
        return out
    return converge_helper

append_=op("y+[x]")
α=append=ad(lambda f:f >> append_|fork)


# standard operators        
_in_=op("x in y")


# standard functions
import random
runif_=fn(lambda n:[random.random() for nn in range(n)])
sum_=fn(sum)
len_=fn(len)
p = Print = fn(print)
range_=fn(range)
_range_=op("range(x,y)")
int_=fn(int)
import math
log_=fn(math.log)
sin_=fn(math.sin)
cos_=fn(math.cos)
exp_=fn(math.exp)
sorted_=fn(sorted)


abs_=fn(abs)
all_=fn(all)
any_=fn(any)
str_=fn(str)
filter_=fn(filter)
float_=fn(float)
repr_=fn(repr)

#Floor
#Ceil
#Sign
not_=fn("not x")
@op
def _if_(x,y):
    return [x[i] for i in range(len(x)) if y[i]]
@op
def _unless_(x,y):
    return [x[i] for i in range(len(x)) if not y[i]]

# greek shortcuts
ψ=φ=fork
µ=flatmap
ω=insert=ins
rµ=rmap
lµ=lmap
rlµ=rlmap
τ=table
ε=_in_
χ=runif_
Σ=sum_
Λ=len_
Ξ=range_

# compute all primes smaller than N
# [i for i in Ξ(N) if not i>> ψ(ε<<τ(_*_)@ψ<<Ξ)]
# [i for i in N>>Ξ if not i in i>>Ξ>>τ(_*_)@ψ ]
# pure python
# [k for k in range(100) if not (k in [i*j for i in range(k) for j in range(k)])]
# pure point-free
# N >>ψ(Ξ >>_unless_<< ψ( ε<< τ(_*_)@ψ <<Ξ )@µ<<Ξ)
# [i for i in range(N) if not i in table(_*_)@fork<<range(i)]
# Fibonacci
# Fib=α(_[-1] + _[-2])
# [1,1] >> Fib@N
# [1,1] >> α(_[-1]+_[-2])@N
# compute pi
# 1000000 >> ψ( ψ(χ>>op("(x**2+y**2)**0.5<1")@rlµ<<χ)>>Σ*4>> _/_)
# 1000000 >> ψ(ψ(χ>>rlµ(_**2>>_+_<<_**2>>_**0.5>>(_<1))<<χ) >> Σ*4 >> _/_)
# N=100000; sum([sqrt(random()**2+random()**2) < 1 for i in range(N)])/N*4
# N >> range_ >> fn("(random()**2+random()**2)**0.5 < 1")@µ >> sum_/N*4)
