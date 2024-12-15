# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'  

urlpatterns = [
    path('', views.catalog_home, name='catalog_home'),  
    path('category/<int:category_id>/', views.category_items, name='category_items'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),  
    path('add-subcategory/', views.add_subcategory, name='add_subcategory'),  
    path('rate/<int:product_id>/', views.submit_rating, name='submit_rating'),
]


