from django.db import models

# Create your models here.

class crop(models.Model):
    crop_name = models.CharField(max_length= 100)
    crop_part = models.CharField(max_length=50,default='Whole plant')
    disease_name = models.CharField(max_length= 100,null=True)
    disease_spread = models.TextField(null=True)
    disease_control = models.TextField(null=True)
    disease_fertilizers = models.TextField(null=True)
    image_crop = models.ImageField(upload_to = 'images',null = True)
    image_disease = models.ImageField(upload_to = 'images',null = True)

    def __str__(self):
        return self.crop_part + '   of   ' + self.crop_name 
    
class plant(models.Model):
    crop_name = models.CharField(max_length= 100)
    image_crop = models.ImageField(upload_to = 'images',null = True)
    
    def __str__(self):
        return self.crop_name


    

