class fn:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        print("ror")
    def __or__(self, other):
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
            return fn(lambda x,self=self,other=other:self.function(other,x))
    def __call__(self, value1, value2):
        return self.function(value1, value2)
class ad:
    def __init__(self, function):
        self.function = function
        
Sqr=fn(lambda x:x**2)
Sqrt=fn(lambda x:x**0.5)
p = Print = fn(print)
Add=op(lambda x,y:x+y)
Div=op(lambda x,y:x/y)
Gt=op(lambda x,y:x>y)

fork=ad(lambda f: fn(lambda x,f=f:f.function(x,x)))
flatmap=ad(lambda f: fn(lambda x,f=f: [f.function(i) for i in x]))
deepmap=ad(lambda f:f)
insert=ad(lambda f:f)
table=ad(lambda f:f)


Sum=fn(sum)
Len=fn(len)
Range=fn(range)

(Add|fork)<<3 >>p
Avg= Sum >>Div<< Len|fork
Ranfge(5) >> Avg >>p
Range(5) >>((Sum>>Div<<Len)|fork) >>p
sum(range(5))/5. >>p
[Sqr(i) for i in range(5)] >>p
range(5) >>(Sqr|flatmap) >>p
range(5) >>((Sqr>>Add<<Sqrt)|fork|flatmap) >>p
range(5) >>(fn(lambda x: x**2+x**0.5)|flatmap) >>p

dist= (Sqr>>Add<<Sqr)>>Sqrt
dist(3,4) >>p

5>>(Add>>Sqrt)<<4 >>p
print(2>>Gt<<3)
(Sqr>>Add<<Sqr)(3,4) >>Sqrt>>p
p<<Sqr<<Sqr<<Sqrt<<4
3>>Sqr>>Sqrt>>p
