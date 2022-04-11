import json
import time
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from modules.user.models import Staffs
from modules.serializers import StaffLoginSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.core import serializers



@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def staff_login(request):
	time.sleep(1)
	username = request.POST.get('uname')
	password = request.POST.get('passw')
	user = authenticate(username=username, password=password)
	if user:
		userializer = StaffLoginSerializer(user, read_only=True)
		data = userializer.data
		data['api_token'] = Token.objects.get(user=user).pk
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'errorCode': 403, 'errorMsg': 'Invalid Credentials.'}), content_type="application/json")   



@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def token_verify(request):
	qaction = request.GET.get('action', '')
	if qaction == 'check-token':
		qtoken = request.GET.get('token', '')
		try:
			token = Token.objects.get(pk=qtoken)
			return Response(status=status.HTTP_200_OK)
		except:
			pass
	return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def index_page(request):
	return HttpResponse(":)", content_type="text/html")