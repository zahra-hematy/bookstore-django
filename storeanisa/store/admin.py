from pyexpat import model
from django.contrib import admin

from store.models import Book

# Register your models here.
from .models import *

class BookAdmin(admin.ModelAdmin):
     readonly_fields=['creat_user']
     def save_model(self, request, obj, form, change):
         obj.create_user = request.user
         return super().save_model(request, obj, form, change)

class AuthorAdmin(admin.ModelAdmin):
     readonly_fields=['creat_user']
class BookReqAdmin(admin.ModelAdmin):
     list_display=['date', 'name', 'author','number_of_requests']
class InvoiceAdmin(admin.ModelAdmin):
     ...
class PaymentAdmin(admin.ModelAdmin):
     ...

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookRequest, BookReqAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
