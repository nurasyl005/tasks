import inspect

def strict(func):
    sig = inspect.signature(func)
    annotations = func.__annotations__

    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        
        for name, value in bound.arguments.items():
            expected_type = annotations.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(f"Argument '{name}' must be {expected_type.__name__}, got {type(value).__name__}")
        return func(*args, **kwargs)
    
    return wrapper