
from symfit import Poly, variables, parameters, Model, Fit
import matplotlib.pyplot as plt
import numpy as np
ns = 64 
nl = 64

## make the x and y array for surface fitting
###
# z = c0 + c1 x + c2 y + c3 xy + c4 xx + c5 yy


class poly2d :
    ns= 0
    nl = 0

    def __init__(self, ns, nl) :
        self.ns = ns
        self.nl = nl

        x = np.linspace(0, ns, num=ns)
        y = np.linspace(0, nl, num=nl)
        self.Y, self.X = np.meshgrid(x, y)


    def fit (self, inarr) :
        inarr_flatten = inarr.flatten()
        x,y,z = variables('x,y,z')
        c0,c1,c2,c3,c4,c5 = parameters('c0,c1,c2,c3,c4,c5')
        model_dict={
            z: Poly({(0,0):c0, (1,0):c1, (0,1):c2, (1,1):c3,
                     (2,0):c4, (0,2):c5},x,y).as_expr()
        }
        model=Model(model_dict)
        newx = self.X.flatten()
        newy = self.Y.flatten()
        fit = Fit(model,x=newx,y=newy, z=inarr_flatten)
        fit_result = fit.execute()
        print (fit_result)
        self.zfit = (model(x=newx, y=newy, **fit_result.params).z).reshape(64,64)
        #self.inarr_sub = self.inar



