from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField()
    price       = models.DecimalField(max_digits=8, decimal_places=2)

    image = models.ImageField(upload_to='products/')
    info_pdf = models.FileField(upload_to='product_pdfs/')

    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    occasion    = models.CharField(max_length=100, blank=True)
    flavor      = models.CharField(max_length=100, blank=True)
    size        = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.filter(is_active=True)
        if not reviews:
            return 0
        return sum(r.stars for r in reviews) / reviews.count()

class Review(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text       = models.TextField()
    stars      = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_active  = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'user')  # eine Bewertung pro User pro Produkt

    def __str__(self):
        return f"{self.user} – {self.product} ({self.stars}★)"

    def helpful_count(self):
        return self.votes.filter(vote_type='helpful').count()

    def not_helpful_count(self):
        return self.votes.filter(vote_type='not_helpful').count()

class ReviewVote(models.Model):
    VOTE_CHOICES = [('helpful', 'Hilfreich'), ('not_helpful', 'Nicht hilfreich')]
    review    = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=20, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('review', 'user')  # eine Stimme pro User pro Bewertung

class ReviewReport(models.Model):
    review     = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason     = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')  # einmal melden pro User pro Bewertung

class Cart(models.Model):
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def subtotal(self):
        return self.product.price * self.quantity