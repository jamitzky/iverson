class fn:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        print("ror")
    def __or__(self, other):
        return other.function(self)
    def __matmul__(self, other):
        #print("self@ad")
        return other.function(self)
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
def insert(f):
    @fn
    def insert_helper(x):
        s0=f(x[0],x[1])
        for xx in x[2:]:
            s0=f(s0,xx)
        return s0
    return insert_helper
rmap=ad(lambda f: op(lambda x,y,f=f: [f.function(x,i) for i in y]))
lmap=ad(lambda f: op(lambda x,y,f=f: [f.function(i,y) for i in x]))
table=rlmap=ad(lambda f: op(lambda x,y,f=f: [f.function(i,j) for i in x for j in y]))
rev=ad(lambda f: op(lambda x,y,f=f:f.function(y,x)))
splitjoin=ad(lambda f:f)

# standard operators        
Add=op(lambda x,y:x+y)
Sub=op(lambda x,y:x-y)
Mul=op(lambda x,y:x*y)
Div=op(lambda x,y:x/y)
Pow=op(lambda x,y:x**y)

Gt=op(lambda x,y:x>y)
Lt=op(lambda x,y:x<y)
Eq=op(lambda x,y:x==y)

o={"+":Add,"-":Sub,"*":Mul,"/":Div,"**":Pow,">":Gt,"<":Lt,"==":Eq}

# standard functions
Sum=fn(sum)
Len=fn(len)
p = Print = fn(print)
Range=fn(range)
Sqr=fn(lambda x:x**2)
Sqrt=fn(lambda x:x**0.5)
#Floor
#Ceil
#Sign
#Sin
#Cos
#Exp
