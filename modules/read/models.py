from django.db import models
from modules.node.models import Nodes


class ReadingsSensor(models.Model):
	node 				=	models.ForeignKey(Nodes, on_delete=models.SET_NULL, related_name='node_sensor', null=True)	
	dust1				=	models.DecimalField(decimal_places=2, max_digits=8)
	dust2				=	models.DecimalField(decimal_places=2, max_digits=8)
	stat				=	models.IntegerField(blank=True, default=1)
	created_at 			= 	models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at 			= 	models.DateTimeField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return '%s' % (self.node.name)

	class Meta:
		db_table 				= 	"readings_sensor"
		verbose_name_plural		= 	"Readings Sensor"



class ReadingsPower(models.Model):
	node 				=	models.ForeignKey(Nodes, on_delete=models.SET_NULL, related_name='node_power', null=True)	
	power_in			=	models.DecimalField(decimal_places=2, max_digits=8)
	power_ex			=	models.DecimalField(decimal_places=2, max_digits=8)
	created_at 			= 	models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at 			= 	models.DateTimeField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return '%s' % (self.node.name)

	class Meta:
		db_table 				= 	"readings_power"
		verbose_name_plural		= 	"Readings Power"







