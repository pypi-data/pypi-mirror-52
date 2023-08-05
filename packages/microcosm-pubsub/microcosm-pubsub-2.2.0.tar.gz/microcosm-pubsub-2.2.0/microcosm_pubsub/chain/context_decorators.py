from functools import WRAPPER_ASSIGNMENTS, wraps
from inspect import Parameter, Signature, signature

from microcosm_pubsub.chain.decorators import BINDS, EXTRACTS


DEFAULT_ASSIGNED = (EXTRACTS, BINDS)
EXTRACT_PREFIX = "extract_"


def get_positional_args(func):
    """
    Returns all the POSITIONAL argument names of a function
    * If func is a method, do not return "self" argument
    * Handle wrapped functions too

    """
    return [
        (arg, parameter.default)
        for arg, parameter
        in signature(func).parameters.items()
        if parameter.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
    ]


def get_from_context(context, func, assigned=DEFAULT_ASSIGNED):
    """
    Decorate a function - pass to the function the relevant arguments
    from a context (dictionary) - based on the function arg names

    """
    positional_args = get_positional_args(func)

    @wraps(func, assigned=assigned + WRAPPER_ASSIGNMENTS)
    def decorate(*args, **kwargs):
        context_kwargs = {
            arg_name: (context[arg_name] if default is Signature.empty else context.get(arg_name, default))
            for arg_name, default in positional_args[len(args):]
            if arg_name not in kwargs
        }
        return func(*args, **kwargs, **context_kwargs)
    return decorate


def save_to_context(context, func, assigned=DEFAULT_ASSIGNED):
    """
    Decorate a function - save to a context (dictionary) the function return value
    if the function is marked by @extracts decorator

    """
    extracts = getattr(func, EXTRACTS, None)
    if not extracts:
        return func
    extracts_one_value = len(extracts) == 1

    @wraps(func, assigned=assigned + WRAPPER_ASSIGNMENTS)
    def decorate(*args, **kwargs):
        value = func(*args, **kwargs)
        if extracts_one_value:
            value = [value]
        for index, name in enumerate(extracts):
            context[name] = value[index]
        return value
    return decorate


def save_to_context_by_func_name(context, func, assigned=DEFAULT_ASSIGNED):
    """
    Decorate a function - save to a context (dictionary) the function return value
    if the function is not signed by EXTRACTS and it's name starts with "extract_"

    """
    if (
        hasattr(func, EXTRACTS) or
        not hasattr(func, "__name__") or
        not func.__name__.startswith(EXTRACT_PREFIX)
    ):
        return func
    name = func.__name__[len(EXTRACT_PREFIX):]

    @wraps(func, assigned=assigned + WRAPPER_ASSIGNMENTS)
    def decorate(*args, **kwargs):
        value = func(*args, **kwargs)
        context[name] = value
        return value
    return decorate


def temporarily_replace_context_keys(context, func, assigned=DEFAULT_ASSIGNED):
    """
    Decorate a function - temporarily updates the context keys while running the function
    Updates the context if the function is marked by @binds decorator.

    """
    binds = getattr(func, BINDS, None)
    if not binds:
        return func

    @wraps(func, assigned=assigned + WRAPPER_ASSIGNMENTS)
    def decorate(*args, **kwargs):
        for old_key, new_key in binds.items():
            if old_key not in context:
                raise KeyError(f"Variable '{old_key}'' not set")
            if new_key in context:
                raise ValueError(f"Variable '{new_key}'' already set")
        try:
            for old_key, new_key in binds.items():
                context[new_key] = context.pop(old_key)
            return func(*args, **kwargs)
        finally:
            for old_key, new_key in binds.items():
                context[old_key] = context.pop(new_key)
    return decorate
