
a = 0.8
r = 0.01
r2 = 0.03
W = 100
R = []
for _ in range(100):
    R.append((1+r)*a+(1-a)*(1+r2))

    
print(R)

for r in R:
    W*=r

print(W)