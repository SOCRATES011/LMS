from django.urls import path
from product.views import Products, AddProduct, EditProduct, delete_product
urlpatterns = [
    path('', Products.as_view(), name='products'),
    path('add_product', AddProduct.as_view(), name= 'add_product'),
    path('edit_product/<str:prod_id>', EditProduct.as_view(), name='edit_product'),
    path('delete_product/<str:prod_id>', delete_product, name='delete_product')

]