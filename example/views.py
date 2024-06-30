from django.http import JsonResponse
from src.data.example.get_example import (
    GetExampleParameter,
    GetExampleUseCase,
)

def example(request):
    if request.method == 'GET':
        use_case = GetExampleUseCase()
        parameter = GetExampleParameter(id=mock_entity["id"], company_id=company_id)
        response = use_case.proceed(parameter)
        return JsonResponse({
            'message': 'Hello, world!'
        })