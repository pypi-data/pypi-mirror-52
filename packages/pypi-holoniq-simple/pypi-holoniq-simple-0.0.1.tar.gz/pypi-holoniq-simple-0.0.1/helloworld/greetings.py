
def say_hello(name=None):
    """Return a greeting to the caller

    Returns "Hello ..." or "Hello, World!" if a name is not supplied
    
    Keyword Arguments:
        name {str} -- The callers name (default: {None})
    
    Returns:
        str -- A simple greeting
    """


    if name is None:
        return "Hello, World!"
    else:
        return f"Hello, {name}!"
