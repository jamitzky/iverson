class fn:
    def __init__(self, function):
        self.function = function
    def __matmul__(self, other):
        #print("fn@other")
        return other.function(self)
    def __rrshift__(self, other):
        #print("fn >> self")
        if type(other)==fn:
            return fn(lambda x,self=self,other=other: self.function(other.function(x)))
        elif type(other)==op:
            return op(lambda x,y,self=self,other=other: self.function(other.function(x,y)))
        else:
            return self.function(other)
    def __lshift__(self, other):
        #print("fn << other")
        if type(other)==fn:
            return fn(lambda x,self=self,other=other: self.function(other.function(x)))
        else:
            return self.function(other)
    def __call__(self, value):
        #print("fn(value)")
        return self.function(value)
class op:
    def __init__(self, function):
        self.function = function
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
            return fn(lambda x,self=self,other=other:self.function(other,x))
    def __call__(self, value1, value2):
        #print("op(value1,value2)")
        return self.function(value1, value2)
class ad:
    def __init__(self, function):
        self.function = function
