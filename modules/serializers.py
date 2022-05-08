import datetime
from django.db.models import Q
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from modules.node.models import Nodes
from modules.read.models import ReadingsSensor, ReadingsPower
from modules.note.models import Notifications
from modules.user.models import Staffs


class NodeListSerializer(ModelSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.get('context', {}).get('request')
		str_fields = request.GET.get('node_fields', '') if request else None
		fields = str_fields.split(',') if str_fields else None
		super(self.__class__, self).__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	read_sensor 			= 	SerializerMethodField('get_read_sensor')
	read_power 				= 	SerializerMethodField('get_read_sensor')

	def get_read_sensor(self, obj):
		request 			= 	self.context.get('request')
		listerStart 		= 	int(request.GET.get('listerStart1', 0))
		listerLimit 		= 	int(request.GET.get('listerLimit1', 50))
		offset 				= 	listerStart*listerLimit
		qfilter1 			= 	request.GET.get('filter1', 'with-last-read')
		is_many				=	False
		readings 			= 	[]
		if qfilter1 == 'with-all-read':
			is_many			=	True
			readings 			=	ReadingsSensor.objects.filter(node=obj).order_by('-created_at')[offset:offset+listerLimit]
		else:
			readings 			=	ReadingsSensor.objects.filter(node=obj).order_by('-created_at').first()
		serializer_context 	= 	{'request': request }
		serializer 			= 	ReadingSensorListSerializer(readings, many=is_many, context=serializer_context)
		return serializer.data


	read_power 				= 	SerializerMethodField('get_read_sensor')

	def get_read_power(self, obj):
		request 			= 	self.context.get('request')
		listerStart 		= 	int(request.GET.get('listerStart1', 0))
		listerLimit 		= 	int(request.GET.get('listerLimit1', 50))
		offset 				= 	listerStart*listerLimit
		qfilter1 			= 	request.GET.get('filter1', 'with-last-read')
		is_many				=	False
		if qfilter1 == 'with-all-read':
			is_many			=	True
			readings 			=	ReadingsPower.objects.filter(node=obj).order_by('-created_at')[offset:offset+listerLimit]
		else:
			readings 			=	ReadingsPower.objects.filter(node=obj).order_by('-created_at').first()
		serializer_context 	= 	{'request': request }
		serializer 			= 	ReadingPowerListSerializer(readings, many=is_many, context=serializer_context)
		return serializer.data

	class Meta:
		model 		= 	Nodes
		fields 		= 	'__all__'



class NodeCreateSerializer(ModelSerializer):
	class Meta:
		model 		= 	Nodes
		exclude 	= 	['created_at','updated_at']



class NodeRetrieveSerializer(ModelSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.get('context', {}).get('request')
		str_fields = request.GET.get('node_fields', '') if request else None
		fields = str_fields.split(',') if str_fields else None
		super(self.__class__, self).__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	read 				= 	SerializerMethodField('get_read')

	def get_read(self, obj):
		request 			= 	self.context.get('request')
		listerStart 		= 	int(request.GET.get('listerStart', 0))
		listerLimit 		= 	int(request.GET.get('listerLimit', 25))
		offset 				= 	listerStart*listerLimit
		qstring 			= 	request.GET.get('queryString', '')
		action 				= 	request.GET.get('action', 'list-reading')
		readings 			= 	{}
		many 				=	True
		if action == 'list-reading':
			readings 			=	Readings.objects.filter(node=obj).order_by('-created_at')[offset:offset+listerLimit]
		elif action == 'date-reading':
			d 					= 	qstring.split('-')
			readings 			=	Readings.objects.filter(node=obj, created_at__gte=datetime.datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0), created_at__lte=datetime.datetime(int(d[0]), int(d[1]), int(d[2]), 23, 59, 59)).order_by('-created_at')[offset:offset+listerLimit]	
		else:
			readings 			=	Readings.objects.filter(node=obj).order_by('-created_at')[0]
			many 				= 	False
		
		serializer_context 	= 	{'request': request }
		serializer 			= 	ReadingListSerializer(readings, many=many, context=serializer_context)
		return serializer.data

	class Meta:
		model 		= 	Nodes
		fields 		= 	'__all__'



class ReadingSensorListSerializer(ModelSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.get('context', {}).get('request')
		str_fields = request.GET.get('read_sensor_fields', '') if request else None
		fields = str_fields.split(',') if str_fields else None
		super(self.__class__, self).__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	node 				= 	SerializerMethodField('get_node')

	def get_node(self, obj):
		request 			= 	self.context.get('request')
		serializer_context 	= 	{'request': request }
		nodes 				=	Nodes.objects.get(pk=obj.node.id)
		serializer 			= 	NodeRetrieveSerializer(nodes, context=serializer_context)
		return serializer.data


	class Meta:
		model 		= 	ReadingsSensor
		fields 		= 	'__all__'



class ReadingSensorCreateSerializer(ModelSerializer):
	class Meta:
		model 		= 	ReadingsSensor
		exclude 	= 	['created_at','updated_at']



class ReadingPowerListSerializer(ModelSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.get('context', {}).get('request')
		str_fields = request.GET.get('read_power_fields', '') if request else None
		fields = str_fields.split(',') if str_fields else None
		super(self.__class__, self).__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	node 				= 	SerializerMethodField('get_node')
	#Reading 				= 	SerializerMethodField('get_Reading')

	def get_node(self, obj):
		request 			= 	self.context.get('request')
		serializer_context 	= 	{'request': request }
		nodes 				=	Nodes.objects.get(pk=obj.node.id)
		serializer 			= 	NodeRetrieveSerializer(nodes, context=serializer_context)
		return serializer.data


	class Meta:
		model 		= 	ReadingsPower
		fields 		= 	'__all__'



class ReadingPowerCreateSerializer(ModelSerializer):
	class Meta:
		model 		= 	ReadingsPower
		exclude 	= 	['created_at','updated_at']



class NotificationListSerializer(ModelSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.get('context', {}).get('request')
		str_fields = request.GET.get('note_fields', '') if request else None
		fields = str_fields.split(',') if str_fields else None
		super(self.__class__, self).__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	read 				= 	SerializerMethodField('get_read')

	def get_read(self, obj):
		request 			= 	self.context.get('request')
		serializer_context 	= 	{'request': request }
		notes 				=	ReadingsSenor.objects.get(pk=obj.read.id)
		serializer 			= 	ReadingSensorListSerializer(notes, context=serializer_context)
		return serializer.data


	class Meta:
		model 		= 	Notifications
		fields 		= 	'__all__'



class NotificationCreateSerializer(ModelSerializer):
	class Meta:
		model 		= 	Notifications
		exclude 	= 	['created_at','updated_at']


class StaffLoginSerializer(ModelSerializer):
	class Meta:
		model 		= 	Staffs
		exclude 	= 	['created_at','updated_at']

