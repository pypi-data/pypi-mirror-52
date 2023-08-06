# PMXUtils

Tools for ProgModX

## Mathtools

* construct(expression, var=x)
    Returns a function computing the given expression
    >expression - The mathematical expression to compute, type = string
    >var - The variable used in the mathematical expression, defaults tp 'x', type = string

* computeLists(function,low, high, step=1)
    Returns a touple of two lists containing x values inbetween low and high, and the computed results for y. In the format of (x_list, y_list)
    >low - The lower end of the function limit, type = number
    >high - The upper end of the function limit, type = number
    >function - The mathematical expression to use for y value computation, type = string or function from construct
    >step - The step size in the x value list, defaults to '1', type = number

* newton(function, derivative, tolerance=1e-8, rounding = 3, iterations = 1000)
    Uses Newtons way of finding the root of a function, using the function and its derivative, within the given limits.Returns None if it can't find a solution that satisfies the tolerance after the defined number of terations
    >function - The target mathematical expression, type = string or function from construct
    >derivative - The derivative of the target mathematical expression, type = string or function from construct
    >tolerance - The tolerance for error to speed up computation, defaults to '1e-8', type = number
    >rounding - Rounds the x value for the root to the specified amount of decimals, defaults to '3', type = number
    >iterations - The number of tries, after which the function will end early

* isInbetween(number, limOne, limTwo)
    Returns True if number is inbetween limOne and limTwo, returns False otherwise
    >number - The number to be checked, type = number
    >limOne - The lower limit for which the number is checked, type = number
    >limTwo - The upper limit for which the number is checked, tyoe = number

## Other

* loading
    Loading class
    * start(flavor="loading")
        Starts a loading sequence
        >flavor - The message to be displayed during loading, defaults to 'loading', type = string
    * stop()
        Stops the loading sequence
    * animate()
        DO NOT USE, internal function
