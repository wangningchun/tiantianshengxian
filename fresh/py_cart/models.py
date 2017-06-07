from django.db import models

# Create your models here.

from df_goods.models import *
from fresheveryday.models import *
# Create your models here.
class CartInfo(models.Model):
    goods=models.ForeignKey(GoodsInfo)
    count=models.IntegerField()
    user=models.ForeignKey(FreshInfo)
