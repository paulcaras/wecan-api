import json
import time
import datetime
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, get_list_or_404
from modules.note.models import Notifications
from modules.serializers import NotificationCreateSerializer, NotificationListSerializer


class NotesViewSets(viewsets.ViewSet):
	authentication_classes  =   [TokenAuthentication]
	permission_classes      =   [IsAuthenticated]

	def list(self, request):
		time.sleep(1)
		qaction = request.GET.get('action', 'lister')
		notes = {}
		if qaction == 'lister':
			notes = Notifications.objects.all().order_by('-created_at')
		serializers = NotificationListSerializer(notes, many=True, context={'request':request})
		return Response(serializers.data)


	def create(self, request):
		serializer = NotificationCreateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, request, pk=None):
		try:
			notes = Notifications.objects.get(pk=pk)
			serializers = NotificationListSerializer(notes, context={'request':request})
			return Response(serializers.data)
		except:
			Response(status=status.HTTP_400_BAD_REQUEST)


	def update(self, request, pk=None):
		time.sleep(1)
		queryset        		=   Notifications.objects.get(pk=pk)
		serializer      		=   NotificationCreateSerializer(instance=queryset, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def partial_update(self, request, pk=None):
		pass


	def destroy(self, request, pk=None):
		pass
