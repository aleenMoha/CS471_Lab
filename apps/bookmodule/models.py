from django.db import models

class Book(models.Model):
    title = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50)
    price = models.FloatField(default = 0.0)
    edition = models.SmallIntegerField(default = 1)

class Publisher(models.Model):
  name = models.CharField(max_length=200)
  location = models.CharField(max_length=300)
    
class Author(models.Model):
  name = models.CharField(max_length=200)
  DOB = models.DateField(null=True)
    
class Book2(models.Model):
  title = models.CharField(max_length= 100)
  price = models.FloatField(default=0.0)
  quantity = models.IntegerField(default=1)
  pubdate = models.DateTimeField()
  rating = models.SmallIntegerField(default = 1)
        
  publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)
  authors = models.ManyToManyField(Author)
