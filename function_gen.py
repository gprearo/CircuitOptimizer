# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 21:21:22 2018

@author: PauloAugusto
"""

'''--Function Generator function--
    kind : Can be \_/,\_,_/ or \/, express the shape of the curve
    order: express the order of the curve (linear ,semi-linear ,quadratic , etc)
    args: the point where the curve reaches 0, and the slope
    Example: FunctionGen('\\_/',1,5,3,10,5) will return a function of \_/ shape,
    with the first point at x=5 with a slope of 3 and the second point at x=10
    and with a slope 5. It returns a function with the given characteristics.'''

def function_gen(kind,order,*args):
    def up(x,x0,slope,exp):
        if x<=x0:   return 0
        else:       return (x-x0)**exp*slope
    def down(x,x0,slope,exp):
        if x>=x0:   return 0
        else:       return (x0-x)**exp*slope
    def func(x):
        if kind=='\\_/':
            if   x<=args[0]:    return down(x,args[0],args[1],order)
            elif x>args[2]:     return up(x,args[2],args[3],order)
            return 0
        elif kind=='\\/':
            new_args=('\\_/',order,args[0],args[1],args[0],args[1])
            return function_gen(*new_args)(x)
        elif kind=='/\\':
            new_args=('\\_/',order,args[0],args[1],args[0],args[1])
            return -function_gen(*new_args)(x)
        elif kind=='_/':
            return up(x,args[0],args[1],order)
        elif kind=='\\_':
            return down(x,args[0],args[1],order)
        elif kind=='/_':
            return -down(x,args[0],args[1],order)
        elif kind=='_\\':
            return -up(x,args[0],args[1],order)
    return func
