from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from product.models import Product
from django.contrib import messages

# Create your views here.

class Products(LoginRequiredMixin, View):
    def get(self, request):
        all_products = Product.objects.all().order_by('-created_at')
        context = {
            'all_prod': all_products
        }
        return render(request, 'products.html', context)
    
class AddProduct(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add_product.html')
    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        if not name or not description or not quantity or not price or not image:
            messages.error(request, 'All fields are required')
            return redirect(resolve_url('add_product'))
        try:
            price = int(price)
            quantity = int(quantity)
        except:
             messages.error(request, 'Quantity and price must be integers')
             return redirect(resolve_url('add_product'))
        
        if price < 10000:
             messages.error(request, 'Price too low')
             return redirect(resolve_url('add_product'))
        if quantity < 1:
             messages.error(request, 'Quantity is low')
             return redirect(resolve_url('add_product'))
        Product.objects.create(
            name = name,
            description = description,
            quantity = quantity,
            price = price,
            image = image,
            user = request.user
        )
        messages.success(request, 'Product listed successfully')
        return redirect(resolve_url('products'))
    
class EditProduct(LoginRequiredMixin, View):
    def get(self, request, prod_id):
        product=Product.objects.filter(id=prod_id).first()
        if not product:
            return redirect(resolve_url('products'))
        if product.user !=request.user:
            return redirect(resolve_url('products'))
        context = {'product': product}
        return render(request, 'edit_product.html', context)
    def post(self,request, prod_id):
        product=Product.objects.filter(id=prod_id).first()
        if not product:
            return redirect(resolve_url('products'))
        if product.user !=request.user:
            return redirect(resolve_url('products'))
        # context = {'product': product}
        # return render(request, 'edit_product.html', context)
        name = request.POST.get('name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        quantity = int(quantity)
        if  quantity < 1:
             messages.error(request, 'Quantity is low')
             return redirect(resolve_url('edit_product'))

        price = request.POST.get('price')
        image = request.FILES.get('image')

        product.name = name or product.name
        product.description = description or product.description
        product.price = price or product.price
        product.quantity = quantity or product.quantity
        product.image = image or product.image
        product.save()
        messages.success(request, 'Product successfully updated!')
        return redirect(resolve_url('products'))
    
@login_required
def delete_product(request, prod_id):
    product=Product.objects.filter(id=prod_id).first()
    if not product:
        return redirect(resolve_url('products'))
    if product.user != request.user:
        return redirect(resolve_url('products'))
    product.delete()
    messages.success(request, 'Product successfully deleted!')
    return redirect(resolve_url('products')) 
