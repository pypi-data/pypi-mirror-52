def deep_extend(*args):
    result = None
    for arg in args:
        if isinstance(arg, dict):
            if not isinstance(result, dict):
                result = {}
            for key in arg:
                result[key] = deep_extend(result[key] if key in result else None, arg[key])
        else:
            result = arg
    return result