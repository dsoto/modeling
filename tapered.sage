# variable declarations
var('w')		# width of wedge
var('b1')		# thickness at base of wedge
var('b2')		# thickness at tip of wedge
var('b')		# thickness at arbitrary point on wedge
var('bx')		# thickness as function of x
var('L')		# length of wedge
var('gamma')	# scaled intercept of wedge function
var('gammasub')
var('alphasub')
var('alpha')	# slope of wedge function            	 	
var('E')		# youngs modulus
var('q')		# load
var('a')		# taper function ranging from 0 (tapered to point) to 1 (no taper)
var('c1 c2 c3')			
var('cc1 cc2 cc3')		
var('cond1 cond2 cond3')	

# simplified taper thickness function
bx = alpha*(x+gamma)

# moment of inertia
I = w*b^3/12
Ix = I.substitute(b = alpha*(x+gamma))

# integrals to get general solution
f2 = (integral(-q,x)+c1)/E/Ix
f1 = integral(f2,x) + c2
f = integral(f1,x) + c3

# print out general solution
print('shape function with integration constants')
print(f)
print latex(f)
# solve for constants
cond1 = solve(f2.substitute(x=L),c1)
cond2 = solve(f1.substitute(x=0),c2)
cond3 = solve(f.substitute(x=0),c3)
cc1=cond1[0].rhs() # get value from solution
cc2=cond2[0].rhs()
cc3=cond3[0].rhs()
f = f.substitute(c3=cc3)
f = f.substitute(c2=cc2)
f = f.substitute(c1=cc1)

print('shape function particular solution')
print(f)
show(f)

f = f.substitute(x=L)
alphasub = (b2-b1)/L
gammasub = b1*L/(b2-b1)
f = f.substitute(gamma = gammasub,alpha=alphasub)
f = f.substitute(b2 = a*b1)

print('shape function with b1 b2 substitutions and simplified')
f=f.simplify_rational()
print(f)
show(f)