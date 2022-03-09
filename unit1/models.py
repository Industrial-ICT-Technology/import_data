from django.db import models


# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_number = models.CharField(max_length=256)
    category_product = models.CharField(max_length=256)
    review_content = models.TextField()
    first_status = models.BooleanField()
    second_status = models.BooleanField()
    dummy_status = models.BooleanField()
    first_labeled_id = models.CharField(max_length=256)
    second_labeled_id = models.CharField(max_length=256)

    def __str__(self):
        return str(self.review_id) + ' - ' + str(self.category_product)
