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
from modules.node.models import Nodes
from modules.read.models import ReadingsSensor, ReadingsSensor
from modules.serializers import NodeCreateSerializer, NodeListSerializer, NodeRetrieveSerializer

class NodesViewSets(viewsets.ViewSet):
	authentication_classes  =   [TokenAuthentication]
	permission_classes      =   [IsAuthenticated]

	def list(self, request):
		time.sleep(1)
		qaction = request.GET.get('action', 'lister')
		qfilter = request.GET.get('filter', 'list-nodes')
		nodes = {}
		if qaction == 'lister':
			if qfilter == 'list-nodes':
				nodes = Nodes.objects.all().order_by('-created_at')
			elif qfilter == 'active-nodes':
				time_threshold = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=3)
				reads = ReadingsSensor.objects.filter(created_at__gt=time_threshold).values_list('node_id', flat=True).distinct('node_id')
				nodes = Nodes.objects.filter(id__in=reads)
		elif qaction == 'finder':
			qstring = request.GET.get('queryString', '')
			nodes = Nodes.objects.filter(name__icontains=qstring)
		serializers = NodeListSerializer(nodes, many=True, context={'request':request})
		return Response(serializers.data)


	def create(self, request):
		serializer = NodeCreateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, request, pk=None):
		try:
			nodes = Nodes.objects.get(pk=pk)
			serializers = NodeRetrieveSerializer(nodes, context={'request':request})
			return Response(serializers.data)
		except:
			Response(status=status.HTTP_400_BAD_REQUEST)


	def update(self, request, pk=None):
		time.sleep(1)
		queryset        		=   Nodes.objects.get(pk=pk)
		serializer      		=   NodeCreateSerializer(instance=queryset, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def partial_update(self, request, pk=None):
		pass


	def destroy(self, request, pk=None):
		pass



@api_view(['POST'])
@permission_classes([AllowAny])
def node_maps(request, format=None):
	if request.data['coord_lat'] > 0 and request.data['coord_lng'] > 0:
		try:
			node = Nodes.objects.filter(c_id=request.data['c_id']).update(
						coord_lat=request.data['coord_lat'],
						coord_lng=request.data['coord_lng']
					)
			return Response(status=status.HTTP_200_OK)
		except:
			pass
	return Response(status=status.HTTP_400_BAD_REQUEST)