class fn:
    def __init__(self, function):
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
            return self.function(other)
    def __lshift__(self, other):
        #print("fn self<<other")
        if type(other)==fn:
            return fn(lambda x,self=self,other=other: self.function(other.function(x)))
        else:
            return self.function(other)
    def __call__(self, value):
        return self.function(value)
class op:
    def __init__(self, function):
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
    def __init__(self, function):
        self.function = function
    
# adverbs definition
fork=ad(lambda f: fn(lambda x,f=f:f.function(x,x)))
flatmap=ad(lambda f: fn(lambda x,f=f: [f.function(i) for i in x]))
deepmap=ad(lambda f:f)
#insert=ad(lambda f:f)
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

splitjoin=ad(lambda f:f)
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

# standard operators        
Add=op(lambda x,y:x+y)
_add=Add
Sub=op(lambda x,y:x-y)
_sub=Sub
Mul=op(lambda x,y:x*y)
_mul=Mul
Div=op(lambda x,y:x/y)
_div=Div
Pow=op(lambda x,y:x**y)
_pow=Pow

Gt=op(lambda x,y:x>y)
_gt=Gt
Lt=op(lambda x,y:x<y)
_lt=Lt
Eq=op(lambda x,y:x==y)
_eq=Eq

o={"+":Add,"-":Sub,"*":Mul,"/":Div,"**":Pow,">":Gt,"<":Lt,"==":Eq}

# standard functions
Sum=fn(sum)
_sum=Sum
Len=fn(len)
_len=Len
p = Print = fn(print)
Range=fn(range)
_range=Range
Sqr=fn(lambda x:x**2)
_sqr=Sqr
Sqrt=fn(lambda x:x**0.5)
_sqrt=Sqrt
_int=fn(int)
import math
_log=fn(math.log)
_sin=fn(math.sin)
_cos=fn(math.cos)
#Floor
#Ceil
#Sign
#Sin
#Cos
#Exp
Get=op(lambda n,x:x[n])
_get=Get
Append=op(lambda val,x:x+[val])
_append=Append
append=ad(lambda f:f >>_append|fork)
