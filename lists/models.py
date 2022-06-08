from django.db import models

class List(models.Model):
    
    pass

class Item(models.Model):
    
    text = models.TextField(default='') # default value required
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

