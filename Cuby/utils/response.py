from django.http import JsonResponse


def JSR(*keys):
    def decorator(request):
        def wrapper(*args, **kw):
            ret = request(*args, **kw)
            if isinstance(ret, int):
                ret = [ret]
            values = list(ret)
            [values.append('') for _ in range(len(keys) - len(values))]
            return JsonResponse(dict(zip(keys, values)))
        return wrapper
    return decorator


def single_value_jsr(request):
    def wrapper(*args, **kw):
        return JsonResponse({'status': request(*args, **kw)})
    
    return wrapper


def dict_jsr(request):
    def wrapper(*args, **kw):
        return JsonResponse(request(*args, **kw))
    
    return wrapper
