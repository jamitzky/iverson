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

Range(10) >> (o[">"]<<2)@flatmap

#IsPrime = (Range >> o("*")@table@fork >> Flatten >> o("=")@flatmap |fork) >> o("+")@ins
#IsPrime = (Range >> Mul@ta@fo >> Flatten >> Eq@fl |fo) >> Add@ins

#Avg = o("+")@insert >> o("/") << Len |fork
#Avg = Sum >> Div << Len | fo

#Fib = o("+=") << (o("[",-1)>>o("+")<<o("[",-2)|fork)
#Fib = IAdd << (Getitem(-1)>>Add<<Getitem(-2)|fo)
#Fib = fn(lambda x: x.append(x[-1]+x[-2]))
#[1,1] >> (Fib^N)
