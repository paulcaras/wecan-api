from django.db import models

class Nodes(models.Model):
	c_id				= 	models.IntegerField(null=True, blank=True, default=0)
	name				=	models.CharField(max_length=128, blank=True)
	bin_height			= 	models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, default=60.0)
	bin_offset			= 	models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, default=10.0)
	coord_lat			=	models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True, default=0)
	coord_lng			=	models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True, default=0)
	installed_at 		= 	models.DateField(blank=True, null=True)
	created_at 			= 	models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at 			= 	models.DateTimeField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return '%s' % (self.name)

	class Meta:
		db_table 				= 	"nodes"
		verbose_name_plural		= 	"Nodes"








