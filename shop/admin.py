from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Category, Review, ReviewVote, ReviewReport, Cart, CartItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ReviewVote)
admin.site.register(ReviewReport)
admin.site.register(Cart)
admin.site.register(CartItem)