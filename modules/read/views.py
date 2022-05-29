import json
import time
import datetime
import decimal
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
#from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, get_list_or_404
from modules.read.models import ReadingsSensor, ReadingsPower
from modules.node.models import Nodes
from modules.note.models import Notifications
from modules.serializers import ReadingSensorCreateSerializer, ReadingSensorListSerializer, ReadingPowerCreateSerializer, ReadingPowerListSerializer, NotificationCreateSerializer


class ReadingSensorViewSets(viewsets.ViewSet):
	authentication_classes  =   [TokenAuthentication]
	permission_classes      =   [IsAuthenticated]

	def list(self, request):
		time.sleep(1)
		listerStart 		= 	int(request.GET.get('listerStart', 0))
		listerLimit 		= 	int(request.GET.get('listerLimit', 50))
		offset 				= 	listerStart*listerLimit
		qstring 			= 	request.GET.get('queryString', '')
		reads 				=	{}
		if len(qstring) > 0:
			d = qstring.split('-')
			reads 			=   ReadingsSensor.objects.filter(created_at__gte=datetime.datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0), created_at__lte=datetime.datetime(int(d[0]), int(d[1]), int(d[2]), 23, 59, 59)).order_by('-created_at')[offset:offset+listerLimit]	
		else:
			reads 				=    ReadingsSensor.objects.filter().order_by("-created_at")[offset:offset+listerLimit]
		serializers		    = 	ReadingSensorListSerializer(reads, many=True, context={'request':request})
		return Response(serializers.data)


	def create(self, request):
		time.sleep(2)
		serializer = ReadingSensorCreateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, request, pk=None):
		try:
			queryset = ReadingsSensor.objects.get(pk=pk)
			serializers = ReadingSensorListSerializer(queryset, context={'request':request})
			return Response(serializers.data)
		except:
			Response(status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk=None):
		pass


	def partial_update(self, request, pk=None):
		pass


	def destroy(self, request, pk=None):
		pass



class ReadingPowerViewSets(viewsets.ViewSet):
	authentication_classes  =   [TokenAuthentication]
	permission_classes      =   [IsAuthenticated]

	def list(self, request):
		time.sleep(1)
		listerStart 		= 	int(request.GET.get('listerStart', 0))
		listerLimit 		= 	int(request.GET.get('listerLimit', 50))
		offset 				= 	listerStart*listerLimit
		qstring 			= 	request.GET.get('queryString', '')
		reads 				=	{}
		if len(qstring) > 0:
			reads 			=   ReadingsPower.objects.filter(created_at__icontains=qstring).order_by('-created_at')[offset:offset+listerLimit]	
		else:
			reads 				=    ReadingsPower.objects.filter().order_by("-created_at")[offset:offset+listerLimit]
		serializers		    = 	ReadingPowerListSerializer(reads, many=True, context={'request':request})
		return Response(serializers.data)


	def create(self, request):
		time.sleep(2)
		serializer = ReadingPowerCreateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, request, pk=None):
		try:
			queryset = ReadingsPower.objects.get(pk=pk)
			serializers = ReadingPowerListSerializer(queryset, context={'request':request})
			return Response(serializers.data)
		except:
			Response(status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk=None):
		pass


	def partial_update(self, request, pk=None):
		pass


	def destroy(self, request, pk=None):
		pass



@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def read_sensor_post(request, format=None):
	node = Nodes.objects.get(c_id=request.data['c_id'])
	if node is not None:
		parse_data = { 'node': node.id, 'dust1': round(request.data['dis1'],2), 'dust2': round(request.data['dis2'],2), 'stat': int(request.data['stat'])  }
		read_last = None
		try:
			last_read = ReadingsSensor.objects.filter(node_id=node.id).order_by('-created_at').first()
		except:
			pass
		serializer = ReadingSensorCreateSerializer(data=parse_data)
		if serializer.is_valid():
			read = serializer.save()
			last_notif = None
			try:
				last_notif = Notifications.objects.filter(read__node_id=node.id).order_by('-created_at').first()
			except:
				pass
			notif = { 'read': 0 }
			if last_read is not None:
				if last_read.stat == 1 and parse_data['stat'] == 2 and (last_notif is None or (last_notif is not None and last_notif.note_type != 1)):
					notif = { 'read': read.id, 'note_type': 1 }
				elif last_read.stat == 2 and parse_data['stat'] == 1 and (last_notif is None or (last_notif is not None and last_notif.note_type != 2)):
					notif = { 'read': read.id, 'note_type': 2 }
				if notif['read'] > 0:
					notifs = NotificationCreateSerializer(data=notif)
					if notifs.is_valid():
						notifs.save()
			return Response(status=status.HTTP_200_OK)
	return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def read_power_post(request, format=None):
	node = Nodes.objects.get(c_id=request.data['c_id'])
	if node is not None:
		parse_data = { 'node': node.id, 'power_in': round(request.data['p_in'],2), 'power_ex': round(request.data['p_ex'],2) }
		serializer = ReadingPowerCreateSerializer(data=parse_data)
		if serializer.is_valid():
			serializer.save()
			return Response(status=status.HTTP_200_OK)
	return Response(status=status.HTTP_400_BAD_REQUEST)