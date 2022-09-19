from cgitb import enable
from ctypes.wintypes import MSG
import email
from http import client
from itertools import count
import site
from telnetlib import STATUS
from unittest import result
from cairo import Status
import django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden
from store.models import Book, Contact
from django.contrib.sites.shortcuts import get_current_site
from .forms import ContactUsForm, BookRequestForm
from django import views
from django.db import IntegrityError
from zeep import Client
from .models import Payment, Invoice, InvoiceItem, BookRequest, Book
# Create your views here.


def hello_world(request):
    about_url =reverse('store:about')
    name = request.GET.get('name')
    family=request.GET.get('family')
    age=request.GET.get('age')
    data={
        'name':name,
        'family':family,
        'age':age
    }
    #return HttpResponse('<html><body><b>Hello World</b></body></html>',
    return render(request, 'store/about.html',data)

def StoreHome(request):
    books = Book.objects.all()
    return render(request, 'store/home.html',{ 'objects':books })

# def contact(request):
#     if request.method=="POST":
#         name=request.POST.get('name')
#         name=request.POST.get('email')
#         name=request.POST.get('msg')
#         context={
#             'name':name,
#             'email':email,
#             'msg':MSG
#         }
#         return render(request, 'store/contact-ok.html',context)
#     else:

#         return render(request, 'store/contact.html')

def contact(request):
    if request.method=="POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            obj =Contact()
            obj.name=form.cleaned_data['name']
            obj.name=form.cleaned_data['email']
            obj.name=form.cleaned_data['message']
            obj.save()
            return render(request, 'store/contact-ok.html',{'form':form})
        else:
            return render(request, 'store/contact.html',{'form': form})
    else:
        
        form=ContactUsForm()
        return render(request, 'store/contact.html',{'form': form})

# def bookreq(request):
#     if request.method=="POST":
#         form = BookRequestForm(request.POST)
#         if form.is_valid():
#             obj = form.save()
#             return render(request, 'store/bookreq-ok.html',{'form':form})
#         else:
#             return render(request, 'store/bookreq.html',{'form': form})
#     else:
        
#         form=BookRequestForm()
#         return render(request, 'store/bookreq.html',{'form': form})


class BookRequestView(views.View):
    def get(self, request):
        form=BookRequestForm()
        return render(request, 'store/bookreq.html',{'form': form})
    def post(self, request):
        if request.method=="POST":
            form = BookRequestForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                author = form.cleaned_data.get('author')
                try:
                    obj = BookRequest(name =name, author=author)
                    obj.cover = form.cleaned_data['cover']
                    obj.number_of_requests+=1
                except BookRequest.DoesNotExist:
                    obj = BookRequest(name =name, author=author)
                    obj.cover = form.cleaned_data['cover']         
                obj.save()
                return render(request, 'store/bookreq-ok.html',{'form':form})
            else:
                return render(request, 'store/bookreq.html',{'form': form})
        from django.shortcuts import get_list_or_404


def get_cart_total(request):
    total=0
    cart = request.session.get('cart', {})
    books = Book.objects.filter(id__in=[int(id) for id in cart.keys()])
    for k,v in cart.items():
        book = books.get(id=int(k))
        total += book.price*v
    return total

class Cart(views.View):
    def get(self, request,bid):
        book = get_object_or_404(Book,id=bid, enabled=True )
        cart = request.session.get('cart',{})
        k = str(book.id)
        if k in cart:       
            cart[k] += 1
        else:
            cart[k] = 1
        request.session['cart'] = cart
        request.session['cart_total'] = get_cart_total(request)
        return redirect('store:index')

class CartDetail(views.View):
    def get(self,request):
        cart = request.session.get('cart', {})
        books = Book.objects.filter(id__in=[int(id) for id in cart.keys()])
        c = {}
        for k,v in cart.items():
            book = books.get(id=int(k))
            c[k] = {'book': book, 'count':v}
        total = get_cart_total(request)
        return render(request, 'store/show_cart.html', {'cart':c, 'total': total})

class CartRemoveView(views.View):
    def get (self, request, pk):
        obj = get_object_or_404(Book, pk=pk)
        cart = request.session.get('cart', {})
        id =str(pk)
        if id in cart:
            cart.pop(id)
        request.session['cart'] = cart
        request.session['cart_total'] = get_cart_total(request)
        ref = request.META['HTTP_REFERER']
        if not ref:
            ref = 'store:show_cart'
        return redirect(ref)

class InvoiceCreateView(LoginRequiredMixin,views.View):
    def get (self, request):
        # global invoice
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('store:index')
        books = Book.objects.filter(id__in=[int(id) for id in cart.keys()])
        invoice = Invoice(user=request.user)
        invoice.save()
        total = 0
        for k,v in cart.items():
            book = books.get(pk=k)
            count = v
            total += book.price * count
            item = InvoiceItem(title=book.title, price=book.price, count=count, invoice=invoice, book=book)
            item.save()
        invoice.total = total
        invoice.save()
        return redirect('store:invoce_show', id=invoice.pk)

        # return render(request, 'store/show_invoice.html', {'id': invoice.pk})

class InvoiceView(LoginRequiredMixin,views.View):
    def get(self, request, id):
        
        invoice = get_object_or_404(Invoice, pk=id)
        return render(request, 'store/show_invoice.html', {'invoice': invoice })

psp_page = 'https://sandbox.zarinpal.com/pg/StartPay/'
merchant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXX'


class PaymentView(LoginRequiredMixin,views.View):
    def get(self, request, invoice_id):

        invoice = get_object_or_404(Invoice, pk=invoice_id)
        if invoice.user !=request.user:
            return HttpResponseForbidden()

        if invoice.state != Invoice.STATE_PENDING:
            return HttpResponseForbidden()

        payment = Payment(invoice=invoice, amount=invoice.total,
                                    description=f'Invoice #{invoice.id}')
        callback = f"http://{site!s}" + reverse('store:payverify')
        client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
        result = client.service.PaymentRequest(MerchantID=merchant,Amount=payment.amount,Description=payment.description, CallbackURL=callback)
        if result.Status == 100:
            payment.authority = result.Authority
            payment.save()
            return redirect(psp_page + payment.authority)
        else:
            payment.state = Payment.STATE_ERROR
            self.save()
            return render(request, 'store/pay_error.html')

class PaymentVerifyView(LoginRequiredMixin,views.View):
    def get(self, request):
        authority = request.Get.get('Authority')
        status = request.Get.get('Status')
        if not authority or not status:
            return HttpResponseForbidden()
        payment = get_object_or_404(Payment, authority=authority, state=Payment.STATE_PENDING)
        if status == "OK":
            client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
            result = client.service.Paymentverification(merchant, payment.authority, payment.amount)
            payment.status = result.Status
            payment.refid = result.RefID
            if result.Status == 100:
                payment.state = Payment.STATE_DONE
                payment.invoice.status = Invoice.STATE_DONE
                payment.save()
                payment.invoice.save()
                request.session['cart'] = {}
                request.session['cart_total'] = 0
                return render(request, 'store/pay_ok.html', {'payment': payment})
            else:
                payment.state = Payment.STATE_ERROR
                payment.save()
                return render(request, 'store/pay_error.html')
