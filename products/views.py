from django.shortcuts import HttpResponse, render, redirect
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, View
from products.forms import ProductCreateForm, ReviewCreateForm
from products.models import Product, Review
from products.costans import PAGINATION_LIMIT


# def hello(request):
#     if request.method == 'GET':
#         return HttpResponse('hello, its my first project! Enjoy! :)')


class HelloCBV(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('hello, its my first project! Enjoy! :)')


# def now_date(request):
#     now_time = datetime.now()
#     if request.method == 'GET':
#         return HttpResponse(now_time)


class DateNowCBV(View):
    now = datetime.now()

    def get(self, request):
        return HttpResponse(self.now)


# def goodbye(request):
#     if request.method == 'GET':
#         return HttpResponse('Goodbye user!')

class GoodbyeCBV(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Goodbye user! ')


# def main_view(request):
#     if request.method == 'GET':
#         return render(request, 'layouts/index.html')


class MainCBV(ListView):
    model = Product
    template_name = 'layouts/index.html'


# def products_view(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         search = request.GET.get('search')
#         page = int(request.GET.get('page', 1))
#
#         '''starts_with, ends_with, icontains'''
#
#         if search:
#             products = products.filter(title__icontains=search) | products.filter(description__icontains=search)
#
#         max_page = products.__len__() / PAGINATION_LIMIT
#         max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)
#
#         '''products splice'''
#         products = products[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]
#
#         context = {
#             'products': products,
#             'user': request.user,
#             'pages': range(1, max_page + 1)
#         }
#         return render(request, 'products/products.html', context=context)


class ProductsCBV(ListView):
    model = Product
    template_name = 'products/products.html'

    def get(self, request, **kwargs):
        products = self.get_queryset()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        '''starts_with, ends_with, icontains'''

        if search:
            products = products.filter(title__icontains=search) | products.filter(description__icontains=search)

        max_page = products.__len__() / PAGINATION_LIMIT
        max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)

        '''products splice'''
        products = products[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]

        context = {
            'products': products,
            'user': request.user,
            'pages': range(1, max_page + 1)
        }
        return render(request, self.template_name, context=context)


def products_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        context = {
            'product': product,
            'review': product.review_set.all(),
            'user': request.user
        }
        return render(request, 'products/detail.html', context=context)


class ProductDetailCBV(DetailView, CreateView):
    model = Product
    template_name = 'products/detail.html'
    form_class = ReviewCreateForm
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'product': self.get_object(),
            'Reviews': Review.objects.filter(product=self.get_object()),
            'form': kwargs.get('form', self.form_class)
        }

    def post(self, request, **kwargs):

        data = request.POST
        form = ReviewCreateForm(data=data)

        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                rate=form.cleaned_data.get('rate'),
                product_id=self.get_object().id
            )
            return redirect(f'/products/{self.get_object().id}/')

        return render(request, self.template_name, context=self.get_context_data(
            form=form
        ))


# def product_create_view(request):
#     if request.method == 'GET':
#         context = {
#             'form': ProductCreateForm
#         }
#         return render(request, 'products/create.html', context=context)
#
#     if request.method == 'POST':
#         form = ProductCreateForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             Product.objects.create(
#                 title=form.cleaned_data.get('title'),
#                 description=form.cleaned_data.get('description'),
#                 quantity=form.cleaned_data.get('quantity'),
#                 image=form.cleaned_data.get('image')
#             )
#             return redirect('/products/')
#         return render(request, 'products/create.html', context={
#             'form': form
#         })

class CreateProductCBV(CreateView, ListView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForm

    def get_context_data(self, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            self.model.objects.create(
                title=form.cleaned_data.get('title')
            )
            return redirect('/products/')
        return render(request, self.template_name, context={self.get_context_data(form=form)})
