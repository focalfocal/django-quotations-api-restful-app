from django.db import models

class Quotation(models.Model):
	
	author = models.CharField(max_length=255,
		default="")
	quot = models.CharField(max_length=2047,
		default="")

	def __str__(self):
		#return self.author  + " pk= " + str(pk)
		return self.author + ": " + self.quot