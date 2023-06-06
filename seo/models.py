from django.db import models

# Create your models here.
class MetaTags(models.Model):
	key = models.CharField(max_length=255)
	arg = models.CharField(max_length=255)






class PageView(models.Model):
	data = models.DateTimeField(auto_now_add=True)
	href = models.CharField(max_length=255)


	class Meta:
		ordering = ["-data","pk"]




from django.contrib.auth.models import User

class Referential(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	def save(self, *args, **kwargs):
		if self.name == None:
			self.name = self.username + self.pk
		return super().save(*args, **kwargs) 


