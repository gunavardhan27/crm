from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.EmailField(null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return str(self.name)
#@receiver(post_save,sender=User)
def create_customer(sender,instance,created,**kwargs):
    if created:
        Customer.objects.create(user=instance,name=instance.username)

#@receiver(post_save,sender=User)
def update_customer(sender,instance,created,**kwargs):
    if created==False:
        instance.customer.save()
    
#tags and models have many-many rship
    
class Tag(models.Model):
    name = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('in door','in door'),
        ('out door','out door')
    )
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True,choices = CATEGORY)
    description = models.CharField(max_length=200,null=True)
    tag = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('delivered','delivered')
    )
    product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add = True,null=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)
    note = models.CharField(max_length=2000,null=True)
    def __str__(self):
        return self.product.name


