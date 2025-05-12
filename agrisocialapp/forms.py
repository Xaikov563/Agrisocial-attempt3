from django import forms
from django.contrib.auth.models import User, models
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Post, Comment, Product

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]


#for creating posts
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'location']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']  # Add fields based on your model
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full p-3 rounded-lg border', 'placeholder': 'What’s on your mind?'}),
        }

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded-lg border', 
                'placeholder': '',
                'style': 'resize: none;',
                }),
        }

#COMMENT FORM

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only include fields you want in the form
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment...'})
        }

class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only include fields you want in the form
        widgets = {
            'content': forms.Textarea(attrs={
            
            'class': 'w-full p-3 rounded-lg border', 
            'placeholder': 'Edit your comment...', 
            'style': 'resize: none;', })
        }


#MARKETPLACE FORM
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'location', 'stock', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Product Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Describe your product...',
                 'style': 'resize: none;',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01',
                'placeholder': 'Price'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Location (optional)'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Stock quantity'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            }),
        }
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Explicitly require fields
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['stock'].required = True

        # Optional: you can also add dynamic requirements like:
        if self.data.get('location') == 'Special Place':
            self.fields['image'].required = True

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'location', 'stock', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Product Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Describe your product...',
                'style': 'resize: none;',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01',
                'placeholder': 'Price'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Location (optional)'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Stock quantity'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        # Explicitly require fields
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['stock'].required = True

        # Optional: you can also add dynamic requirements like:
        if self.data.get('location') == 'Special Place':
            self.fields['image'].required = True