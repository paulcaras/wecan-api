from django.db import models

class Nodes(models.Model):
	chipid				= 	models.BigIntegerField(null=True, blank=True, default=0)
	name				=	models.CharField(max_length=128, blank=True)
	created_at 			= 	models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at 			= 	models.DateTimeField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return '%s' % (self.name)

	class Meta:
		db_table 				= 	"nodes"
		verbose_name_plural		= 	"Nodes"








