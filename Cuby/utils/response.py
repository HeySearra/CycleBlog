from django.http import JsonResponse


def single_value_jsr(request):
    def wrapper(*args, **kw):
        return JsonResponse({'status': request(*args, **kw)})
    
    return wrapper


def dict_jsr(request):
    def wrapper(*args, **kw):
        return JsonResponse(request(*args, **kw))
    
    return wrapper
