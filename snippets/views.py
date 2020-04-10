from rest_framework import status 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create new snippet.
    """
    if request.method == 'GET': # snippets 모두 불러오기
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True) # queryset을 serialize 하기
        return Response(serializer.data) # json으로 return

    elif request.method == 'POST': # snippet 새로 만들기
        serializer = SnippetSerializer(data=request.data) # request.data를 통해 어떤 데이터도 가져올 수 있음
        if serializer.is_valid(): # 성공
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 명확한 status reponse 가능
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 실패

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk) # 특정 snippet 가져오기
    except Snippet.DoesNotExist: # 일치하는 snippet이 없을 경우
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
