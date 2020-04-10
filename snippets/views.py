from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create new snippet.
    """
    if request.method == 'GET': # snippets 모두 불러오기
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True) # queryset을 serialize 하기
        return JsonResponse(serializer.data, safe=False) # json으로 return

    elif request.method == 'POST': # snippet 새로 만들기
        data = JSONParser().parse(request) # python native type으로 parsing
        serializer = SnippetSerializer(data=data) # object instance로 serialize
        if serializer.is_valid(): # 성공
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400) # 실패

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk) # 특정 snippet 가져오기
    except Snippet.DoesNotExist: # 일치하는 snippet이 없을 경우
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
