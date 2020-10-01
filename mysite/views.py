from django.shortcuts import render

#from rest_framework.decorators import api_view
from rest_framework.response import Response
#from rest_framework import status
from .models import Quotation
from .serializers import QuotationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination

class CustomPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.user.has_perm('mysite.add_quotation'):
			return True
		return False

def home(request):
	return render(request, 'mysite/index.html')

#ALL / NEW 
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
@permission_classes([CustomPermission])
def quotation_api_view(request):

	#get all
	if request.method == "GET":
		paginator = PageNumberPagination()
		paginator.page_size = 2  #items per page	
		quotation_objects = Quotation.objects.all()
		result = paginator.paginate_queryset(quotation_objects, request)

		#serializer = QuotationSerializer(Quotation.objects.all(), many=True)  #without pagination
		serializer = QuotationSerializer(result, many=True)
		return Response(serializer.data)

	#create new
	elif request.method == "POST":
		serializer = QuotationSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,
				status=status.HTTP_201_CREATED)
		return Response(serializer.errors,
			status=status.HTTP_400_BAD_REQUEST)

#DETAIL
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([CustomPermission])
def quotation_api_detail_view(request, pk=None):
	
	try:
		quotation = Quotation.objects.get(pk=pk)
	except Quotation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	#get one quotation
	if request.method == 'GET':
		serializer = QuotationSerializer(quotation)
		return Response(serializer.data)
	
	#modify one quotation
	elif request.method == 'PUT':
		serializer = QuotationSerializer(quotation,
			data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		#serializer not valid:	
		return Response(quotation.errors,
			status=status.HTTP_400_BAD_REQUEST)
	
	#delete one quotation  
	elif request.method == 'DELETE':
		quotation.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)