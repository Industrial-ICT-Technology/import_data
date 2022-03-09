from django.db import models

# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_content = models.TextField()

    objects = models.Manager()
