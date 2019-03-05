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
        
sqr=fn(lambda x:x**2)
sqrt=fn(lambda x:x**0.5)
p=fn(print)
plus=op(lambda x,y:x+y)
div=op(lambda x,y:x/y)
gt=op(lambda x,y:x>y)
fork=ad(lambda f: fn(lambda x,f=f:f.function(x,x)))
map=ad(lambda f: fn(lambda x,f=f: [f.function(i) for i in x]))
fold=ad(lambda f:f)
table=ad(lambda f:f)
Sum=fn(sum)
Len=fn(len)

(plus|fork)<<3 >>p
Avg=(Sum>>div<<Len)|fork
Avg(range(5)) >>p
range(5) >>((Sum>>div<<Len)|fork) >>p
sum(range(5))/5. >>p
[sqr(i) for i in range(5)] >>p
range(5) >>(sqr|map) >>p
range(5) >>((sqr>>plus<<sqrt)|fork|map) >>p
range(5) >>(fn(lambda x: x**2+x**0.5)|map) >>p

dist= (sqr>>plus<<sqr)>>sqrt
dist(3,4) >>p

5>>(plus>>sqrt)<<4 >>p
print(2>>gt<<3)
(sqr>>plus<<sqr)(3,4) >>sqrt>>p
p<<sqr<<sqr<<sqrt<<4
3>>sqr>>sqrt>>p
