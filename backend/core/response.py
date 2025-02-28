import json
from django.http import JsonResponse

class Response:
    """
    HTTP Response Helper for Django
    """

    @staticmethod
    def ok(data=None, msg='success operate！', code=200, **kwargs):
        response = {'success': True, 'code': code, 'msg': msg, 'data': data}

        if kwargs:
            response.update(**kwargs)
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

    @staticmethod
    def error(msg=None, code=400):
        return JsonResponse({'success': False, 'code': code, 'msg': msg or 'Failed operate!'})

    @staticmethod
    def error_data(code=400, msg=None, data=None):
        return JsonResponse(
            {'success': False, 'code': code, 'msg': msg or 'Failed operate!', 'data': data or []},
            json_dumps_params={'ensure_ascii': False}
        )
