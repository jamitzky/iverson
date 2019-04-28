#
# (c) Ferdinand Jamitzky 2019
#

class fn:
    __array_priority__=2
    def __init__(self, function):
        """
        sqr=fn("x**2")
        sqrt=fn(lambda x:x**0.5)
        """
        if type(function)==str:
            self.function=eval("lambda x:"+function)
        else:
            self.function = function

    def __matmul__(self, other):
        """
        function decorators:
        f@flatmap  == flatmap(f)            # map sqr to list
        f@4  == f(f(f(f(x))))        # apply f 4 times
        f@g  == f(g(x)) 
        """
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
            return self(other)
        else:
            return self(fn(other))
    def __rshift__(self,other):
        """
        f >> g      # g(f(x))
        f >> (_+_)  # f(x)+y
        """        
        return other(self)
    def __rrshift__(self, other):
        """
        x >> f
        """
        return self(other)
    def __lshift__(self, other):
        """
        f << g      # f(g(x))
        f << x      # f(x)
        """
        #print("fn self<<other")
        return self(other)
    def __call__(self, other=None):
        """
        call fn object like a function
        f(g)(x) =f(g(x))
        """
        if other==None:
            return self.function(None)
        if type(other)==fn:
            return fn(lambda x,self=self,other=other: self.function(other.function(x)))
        if type(other)==op:
            return op(lambda x,y,self=self,other=other: self.function(other.function(x,y)))
        return self.function(other)
    def __add__(self,other):
        """
        f+g (x) = f(x)+g(x)
        """
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
    def __gt__(self,other):
        if type(other)==fn:
            return fn(lambda x:self(x)>other(x))
        else:
            return fn(lambda x:self(x)>other)
    def __lt__(self,other):
        if type(other)==fn:
            return fn(lambda x:self(x)<other(x))
        else:
            return fn(lambda x:self(x)<other)

class op:
    __array_priority__=2    
    def __init__(self, function):
        """
        op("x+y")
        op(lambda x,y:x+y)
        """
        #print(function)
        if type(function)==str:
            #print("string")
            self.function=eval("lambda x,y:"+function)
        else:
            self.function = function
    def __matmul__(self, other):
        """
        apply adverb, eg:
        op("x+y")@fork   # x+x
        """
        #print("self@ad")
        return other.function(self)
    def __rrshift__(self, other):
        """
        f >> op("x+y")  # f(x)+y
        1 >> op("x+y")  # fn("1+x")
        """
        #print("op other>>self")
        return self(other)
    def __rshift__(self,other):
        """
        (_+_) >> f   == f(x+y)
         """
        return other(self)
    def __lshift__(self, other):
        """
        op("x+y") << f  # x+f(y)
        op("x+y") << 2  # fn("x+2")
        """
        #print("op self<<other")
        return self(None,other)
    def __call__(self, value1=None, value2=None):
        """
        curry operator:
        (_+_)(2)(3) == (_+2)(3)=3+2
        (_+_)(2,3) == 2+3
        op(op,op)
        op(op,y)
        op(x,op)
        op(x,y)
        op()
        op(x)
        """
        #print(" op(x,y) and op(x)",value1,value2)
        if value2==None and value1==None:
            return fn(lambda x,self=self: self.function(x,x))
        if value2==None:
            if type(value1)==fn:
                return op(lambda x,y,self=self,value1=value1: self.function(value1(x),y))
            else:
                return fn(lambda x,self=self,value1=value1: self.function(value1,x))
        if value1==None:
            if type(value2)==fn:
                return op(lambda x,y,self=self,value2=value2: self.function(x,value2(y)))
            else:
                return fn(lambda x,self=self,value2=value2: self.function(x,value2))
        if type(value1)==fn and type(value2)==fn:
            return op(lambda x,y,self=self,value1=value1,value2=value2: self.function(value1(x), value2(y)))
        if type(value1)==fn:
            return fn(lambda x,self=self,value1=value1,value2=value2: self.function(value1(x), value2))
        if type(value2)==fn:
            return fn(lambda y,self=self,value1=value1,value2=value2: self.function(value1, value2(y)))
        if type(value1)==op and type(value2)==op:
            return op(lambda x,y,self=self,value1=value1,value2=value2: self.function(value1(x,y), value2(x,y)))
        if type(value1)==op:
            return op(lambda x,y,self=self,value1=value1,value2=value2:self.function(value1(x,y),value2))
        if type(value2)==op:
            return op(lambda x,y,self=self,value1=value1,value2=value2:self.function(value1,value2(x,y)))
        return self.function(value1,value2)
    
    def __add__(self,other):
        "op1 + op2 == op1(x,y)+op2(x,y)"
        if type(other)==op:
            return op(lambda x,y,self=self,other=other:self(x,y)+other(x,y))
        else:
            return op(lambda x,y,self=self,other=other:self(x,y)+other)

    def __sub__(self,other):
        "op1 - op2 == op1(x,y)-op2(x,y)"
        if type(other)==op:
            return op(lambda x,y,self=self,other=other:self(x,y)-other(x,y))
        else:
            return op(lambda x,y,self=self,other=other:self(x,y)-other)

    def __mul__(self,other):
        "op1 * op2 == op1(x,y)*op2(x,y)"
        if type(other)==op:
            return op(lambda x,y,self=self,other=other:self(x,y)*other(x,y))
        else:
            return op(lambda x,y,self=self,other=other:self(x,y)*other)

    def __truediv__(self,other):
        "op1 / op2 == op1(x,y)/op2(x,y)"
        if type(other)==op:
            return op(lambda x,y,self=self,other=other:self(x,y)/other(x,y))
        else:
            return op(lambda x,y,self=self,other=other:self(x,y)/other)
    def __rtruediv__(self,other):
        "op1 / op2 == op1(x,y)/op2(x,y)"
        return op(lambda x,y,self=self,other=other:other/self(x,y))

    def __pow__(self,other):
        "op1 ** op2 == op1(x,y)**op2(x,y)"
        if type(other)==op:
            return op(lambda x,y,self=self,other=other:self(x,y)**other(x,y))
        else:
            return op(lambda x,y,self=self,other=other:self(x,y)**other)

    def __gt__(self,other):
        "op1 > op2 == op1(x,y)>op2(x,y)"
        if type(other)==op:
            return op(lambda x,y,self=self,other=other:self(x,y)>other(x,y))
        else:
            return op(lambda x,y,self=self,other=other:self(x,y)>other)

    def __lt__(self,other):
        "op1 < op2 == op1(x,y)<op2(x,y)"
        if type(other)==op:
            return op(lambda x,y,self=self,other=other:self(x,y)<other(x,y))
        else:
            return op(lambda x,y,self=self,other=other:self(x,y)<other)


        
class ad:
    __array_priority__=2    
    def __init__(self, function):
        """
        """
        self.function = function
    def __call__(self,verb):
        """
        """
        if type(verb)==fn:
            return self.function(verb)
        elif type(verb)==op:
            return self.function(verb)
        else:
            return self.function(fn(verb))
            

# underscore definition
import operator
class uscore:
    __array_priority__=2
    def __init__(self):
        """
        _=uscore()
        """        
        pass
    def __matmul__(self,other):
        return fn(other)
    def __add__(self,other):
        """
        (_+_) == op("x+y")
        (_+2) == op("x+2")        
        """
        if type(other)==uscore:
            return op(operator.__add__)
        else:
            return fn(lambda x,other=other:operator.__add__(x,other))
    def __radd__(self,other):
        """
        (2+_) == op("2+y")
        """
        return fn(lambda x,other=other:operator.__add__(other,x))
    def __sub__(self,other):
        if type(other)==uscore:
            return op(operator.__sub__)
        else:
            return fn(lambda x,other=other:operator.__sub__(x,other))
    def __rsub__(self,other):
        """
        (2-_) == op("2-y")
        """
        return fn(lambda x,other=other:operator.__sub__(other,x))
    def __mul__(self,other):
        if type(other)==uscore:
            return op(operator.__mul__)
        else:
            return fn(lambda x,other=other:operator.__mul__(x,other))
    def __rmul__(self,other):
        """
        (2*_) == op("2*y")
        """
        return fn(lambda x,other=other:operator.__mul__(other,x))
    def __truediv__(self,other):
        if type(other)==uscore:
            return op(operator.__truediv__)
        else:
            return fn(lambda x,other=other:operator.__truediv__(x,other))
    def __rtruediv__(self,other):
        """
        (2/_) == op("2/y")
        """
        return fn(lambda x,other=other:operator.__truediv__(other,x))
    def __pow__(self,other):
        if type(other)==uscore:
            return op(operator.__pow__)
        else:
            return fn(lambda x,other=other:operator.__pow__(x,other))
    def __rpow__(self,other):
        """
        (2**_) == op("2**y")
        """
        return fn(lambda x,other=other:operator.__pow__(other,x))
    def __gt__(self,other):
        if type(other)==uscore:
            return op(operator.__gt__)
        else:
            return fn(lambda x,other=other:operator.__gt__(x,other))
    def __rgt__(self,other):
        """
        (2>_) == op("2>y")
        """
        return fn(lambda x,other=other:operator.__gt__(other,x))
    def __lt__(self,other):
        if type(other)==uscore:
            return op(operator.__lt__)
        else:
            return fn(lambda x,other=other:operator.__lt__(x,other))
    def __rlt__(self,other):
        """
        (2<_) == op("2<y")
        """
        return fn(lambda x,other=other:operator.__lt__(other,x))
    def __eq__(self,other):
        if type(other)==uscore:
            return op(operator.__eq__)
        else:
            return fn(lambda x,other=other:operator.__eq__(x,other))
    def __req__(self,other):
        """
        (2=_) == op("2=y")
        """
        return fn(lambda x,other=other:operator.__eq__(other,x))
    def __in__(self,other):
        "fixme"
        if type(other)==uscore:
            return op(operator.__in__)
        else:
            return fn(lambda x,other=other:operator.__in__(x,other))
    def __getitem__(self,other):
        """
        (_[-1])(x) == x[-1]
        """
        if type(other)==uscore:
            return op(operator.__getitem__)
        else:
            return fn(lambda x,other=other:operator.__getitem__(x,other))
    def __getattr__(self,other):
        """
        "asasasaadada" >> _.split << "a"
        """
        return op(lambda x,y,other=other:getattr(x,other)(y))
    def __call__(self,f1,f2,f3):
        """
        fork J style
        _(_+_, _/_, _-_) == op("(x+y)/(x-y)")
        """
        if type(f1)==op and type(f2)==op and type(f2)==op:
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
zip=rlmap
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
append=ad(lambda f:(f >> append_)())

tee=ad(lambda f:fn(lambda x:[x,f(x)])>>_[0])
_sto=[]
@fn
def sto(x):
    _sto.append(x)
rec=lambda : _sto[-1]
#N=1000; N >> tee(sto) >> R >> µ(_/rec()) >>sin_(X)*cos_(Y)@table@fork >> sum_/rec()**2

# standard operators        
_in_=op("x in y")
to=op(lambda x,y:range(x,y))
# 1>>to(10)
tr=tee(_@print)


# standard functions
import random
runif_=fn(lambda n:[random.random() for nn in range(n)])
sum_=fn(sum)
len_=fn(len)
pr = Print = fn(print)
range_=fn(range)
_range_=op("range(x,y)")
int_=fn(int)
import math
log_=fn(math.log)
sin_=fn(math.sin)
cos_=fn(math.cos)
exp_=fn(math.exp)
sqrt_=fn(math.sqrt)
sorted_=fn(sorted)


abs_=fn(abs)
all_=fn(all)
any_=fn(any)
str_=fn(str)
filter_=op(lambda x,y: [x[i] for i in range(len(x)) if y[i]])
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

# variables
X=op(lambda x,y:x)
Y=op(lambda x,y:y)

# greek shortcuts α, β, γ, δ, ε, η, θ, ζ, ι, κ, λ, μ, ν, ξ, π, ρ, σ, τ, υ, φ, χ, ψ, ω
ψ=fork
µ=flatmap
γ=insert=ins
rµ=rmap
lµ=lmap
rlµ=rlmap
τ=table
ε=_in_

U=runif_
R=fn(lambda x: list(range(x)))
Σ=sum_

Λ=len_
α=X
ω=Y

# compute all primes smaller than N
# pure python
# [k for k in range(100) if not (k in [i*j for i in range(k) for j in range(k)])]
# pure point-free
primes= (R >> _unless_ <<  (_in_ << (X*Y)@table@fork@R)@fork@flatmap@R)@fork
primes=  (_unless_ << (_in_ << table(X*Y)()(R))()@flatmap)()(R)
primes=  (_unless_ << (ε << τ(X*Y)()(R))()@µ)()(R)
primes=  (_unless_ << (ε << τ(X*Y)()@R)()@µ)()@R
10 >> primes >> pr

# Fibonacci
Fib=append(_[-1] + _[-2])
[1,1] >> Fib@10 >> pr

# compute pi
1000>> ( sum_(zip(X**2+Y**2 < 1))(runif_,runif_)() >> (X/Y)*4)() >> pr
1000>> ( sum_(zip(X**2+Y**2 < 1))(U,U)() >> (X/Y)*4)() >> pr

# apyl
1>>to<<10 >> lmap(X/(_@max)(Y))() >> pr

