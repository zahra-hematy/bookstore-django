from distutils.command.upload import upload
from email.policy import default
from tokenize import blank_re
from django.db import models
from matplotlib.pyplot import cla
from isbn_field import ISBNField
from django.contrib.auth.models import User
import os
import uuid 
from datetime import datetime
import attr
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class baseModel(models.Model):
    creat_user = models.DateTimeField(auto_now_add=True)
    modify = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=True)

    class Meta:
        abstract = True

def get_covert_path(obj, fn):
    ex = os.path.splitext(fn)[1]
    uid = uuid.uuid5(uuid.NAMESPACE_URL,f"store-book-{obj.pk}" )
    path =datetime.now().strftime(f"book_covers/%Y/%m/%d/{uid}{ex}")
    return path


class Book(baseModel):
    title = models.CharField(max_length=255) 
    price = models.IntegerField()
    count = models.IntegerField()
    enabled = models.BooleanField(default=True)
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    isbn = ISBNField(null=True, blank=True)
    cover = models.ImageField(upload_to=get_covert_path,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.title} ({self.author.name})"
    
class Author(baseModel):
    name = models.CharField(max_length=255)
    
    def book_count(self):
       return len(self.book_set.count())

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=255)
    email=models.EmailField()
    message=models.TextField()


class BookRequest(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='request_covers/',null=True,blank=True)
    number_of_requests =models.IntegerField(default=1)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('name','author'),
                                            name='name_author_uniq')
        ]    


class Invoice(models.Model):

    STATE_PENDING = 'pending'
    STATE_DONE = 'done'
    STATE_CHOICES = ((STATE_PENDING, 'Pending'),
                    (STATE_DONE, 'Done'))

    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    total = models.IntegerField(default=0)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default=STATE_PENDING)

class InvoiceItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT,
                            related_name="item" )
    price = models.IntegerField()
    count = models.IntegerField(default=1)
    title = models.CharField(max_length=255)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)

class Payment(models.Model):
    STATE_PENDING = 'pending'
    STATE_DONE = 'done'
    STATE_ERROR = 'Error'

    STATE_CHOICES = ((STATE_PENDING, 'Pending'),
                    (STATE_DONE, 'Done'),
                    (STATE_ERROR, 'Error'))

    date = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    amount = models.IntegerField()
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default=STATE_PENDING)
    authority = models.CharField(max_length=36, null=True)
    refid = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)