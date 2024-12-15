from django import forms
from .models import Item, Category, SubCategory

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'image', 'category', 'subcategory']

# Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

# SubCategory Form
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']

# catalog/forms.py

from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review']  # Fields to be displayed in the form
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),  # Radio buttons for rating
            'review': forms.Textarea(attrs={'placeholder': 'Write a review (optional)', 'rows': 4}),
        }
