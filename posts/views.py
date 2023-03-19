from django.shortcuts import HttpResponse, render
from datetime import datetime
from posts.models import Product


def hello(request):
    if request.method == 'GET':
        return HttpResponse('hello, its my first project! Enjoy! :)')


def now_date(request):
    now_time = datetime.now()
    if request.method == 'GET':
        return HttpResponse(now_time)


def goodbye(request):
    if request.method == 'GET':
        return HttpResponse('Goodbye user!')


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'products/products.html', context=context)
