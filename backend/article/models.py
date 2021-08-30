from django.db import models

# Create your models here.
class article(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    about=models.TextField()
    info = models.TextField()
    link = models.URLField(max_length=200)
    image = models.ImageField(upload_to = 'images')
    pub_date=models.DateField('date published',null=True)

    def __str__(self):
        return self.name
    
    
