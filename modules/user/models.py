from django.db import models
from django.contrib.auth.models import AbstractUser

class Staffs(AbstractUser):
	created_at 			= 	models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at 			= 	models.DateTimeField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return '%s' % (self.first_name)

	class Meta:
		db_table 				= 	"staffs"
		verbose_name_plural		= 	"Staffs"







