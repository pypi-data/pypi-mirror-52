"""A set of functions aiding in math for ProgModX"""
from numpy import arange
from math import sin, cos, tan, pi

def construct(expression, var="x"):
    """Returns a function computing the given expression"""
    def f(x):
        return eval(expression.replace(var, "x"))
    return f

def computeLists(low, high, function, step=1):
    """Returns a touple of two lists containing x values inbetween low and high, and the computed results for y.
    In the format of (x_list, y_list)"""
    if type(function) == type(str()):
        function = construct(function)
    return (arange(low, high+1, step), [function(i) for i in arange(low, high+1, step)])