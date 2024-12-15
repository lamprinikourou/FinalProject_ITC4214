from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Category, SubCategory
from .forms import ItemForm, CategoryForm, SubCategoryForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Rating



def catalog_home(request):
    # Fetch categories and subcategories
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    # Get filter parameters from request
    search_query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    selected_category = request.GET.get('category')
    selected_subcategory = request.GET.get('subcategory')

    # Start with all items
    items = Item.objects.all()

    # Apply filters step-by-step
    if selected_category:
        items = items.filter(category_id=selected_category)

    if selected_subcategory:
        items = items.filter(subcategory_id=selected_subcategory)

    if search_query:
        items = items.filter(name__icontains=search_query)

    # Validate and apply price filters
    try:
        if min_price:
            items = items.filter(price__gte=float(min_price))
        
        if max_price:
            items = items.filter(price__lte=float(max_price))
    except ValueError:
        messages.warning(request, "Invalid price range input. Please provide valid numbers.")

    return render(request, 'catalog/catalog_home.html', {
        'categories': categories,
        'subcategories': subcategories,
        'items': items,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
    })


def category_items(request, category_id):
    # Get the selected category
    category = get_object_or_404(Category, id=category_id)

    # Fetch sub-categories for this category
    subcategories = SubCategory.objects.filter(category=category)

    # Filter items based on the selected sub-category (if provided)
    subcategory_id = request.GET.get('subcategory')
    items = Item.objects.filter(category=category)
    if subcategory_id:
        items = items.filter(subcategory_id=subcategory_id)

    return render(request, 'catalog/category_items.html', {
        'category': category,
        'subcategories': subcategories,
        'items': items,
    })



@login_required
def add_product(request):
    # Allow authenticated users to add a new product
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product added successfully!")
            return redirect('catalog:item_detail', item_id=product.id)  # Redirect to the product detail page
    else:
        form = ItemForm()

    return render(request, 'catalog/add_product.html', {'form': form})


# Add Category View
@login_required
def add_category(request):
    if request.user.is_staff:  # Only admin users can add categories
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Category added successfully!")
                return redirect('catalog:catalog_home')
        else:
            form = CategoryForm()
        return render(request, 'catalog/add_category.html', {'form': form})
    else:
        messages.error(request, "You don't have permission to add categories.")
        return redirect('catalog:catalog_home')

# Add SubCategory View
@login_required
def add_subcategory(request):
    if request.user.is_staff:  # Only admin users can add subcategories
        if request.method == 'POST':
            form = SubCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Subcategory added successfully!")
                return redirect('catalog:catalog_home')
        else:
            form = SubCategoryForm()
        return render(request, 'catalog/add_subcategory.html', {'form': form})
    else:
        messages.error(request, "You don't have permission to add subcategories.")
        return redirect('catalog:catalog_home')
    

# catalog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Rating
from .forms import RatingForm

@login_required
def submit_rating(request, product_id):
    # Get the product for which the rating is being submitted
    product = get_object_or_404(Item, id=product_id)
    
    # Check if the user has already rated this product
    existing_rating = Rating.objects.filter(user=request.user, product=product).first()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user  # Assign the user who submitted the rating
            rating.product = product  # Assign the product being rated
            rating.save()
            return redirect('catalog:item_detail', item_id=product.id)  # Redirect to product detail page

    else:
        # If the user has already rated this product, pre-populate the form with the existing rating
        initial_data = {'rating': existing_rating.rating, 'review': existing_rating.review} if existing_rating else {}
        form = RatingForm(initial=initial_data)

    return render(request, 'catalog/submit_rating.html', {'form': form, 'product': product})



from django.db import models  
from django.shortcuts import render, get_object_or_404
from .models import Item, Rating  
from django.db.models import Avg  


def item_detail(request, item_id):
    product = get_object_or_404(Item, id=item_id)
    # Calculate the average rating
    average_rating = product.ratings.aggregate(Avg('rating'))['rating__avg']  # Calculate the average rating
    
    return render(request, 'catalog/item_detail.html', {
        'item': product,
        'average_rating': average_rating,  # Pass average rating to the template
    })

