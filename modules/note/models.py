from django.db import models
from modules.read.models import ReadingsSensor


class Notifications(models.Model):
	NOTE_TYPE 			=	(
								(1, 'FULL'),
								(2, 'EMPTY'),
							)
	read				= 	models.ForeignKey(ReadingsSensor, on_delete=models.SET_NULL, related_name='note_sensor', null=True)	
	note_type			=	models.CharField(max_length=1, choices=NOTE_TYPE, blank=True, default=1)
	is_viewed			= 	models.BooleanField(blank=True, default=False)
	created_at 			= 	models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at 			= 	models.DateTimeField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return '%s - %s' % (self.read.node.name, self.note_type)

	class Meta:
		db_table 				= 	"notifications"
		verbose_name_plural		= 	"Notifications"








