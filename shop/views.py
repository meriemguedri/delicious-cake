from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review, ReviewVote, ReviewReport, Cart, CartItem, Category
from .forms import ReviewForm, ProductForm
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test


def product_list(request):
    query = request.GET.get('q', '')
    min_stars = request.GET.get('stars', '')
    category_id = request.GET.get('category', '')

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category__id=category_id)

    if min_stars:
        products = [p for p in products if p.average_rating() >= int(min_stars)]

    return render(request, 'shop/product_list.html', {
        'products': products,
        'query': query,
        'min_stars': min_stars,
        'categories': categories,
        'selected_category': category_id,
    })


def product_detail(request, pk):
    product     = get_object_or_404(Product, pk=pk)
    reviews     = product.reviews.filter(is_active=True)
    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first() # ob der user hat schon was bewertet oder nicht

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST, instance=user_review) #instance : wenn User schon Review hat → bearbeiten statt neu erstellen
        if form.is_valid():
            review         = form.save(commit=False) # false weil wir noch product und user setzen müssen
            review.product = product
            review.user    = request.user
            review.save()
            return redirect('product_detail', pk=pk) #redirect : nach dem Speichern Seite neu laden
    else:
        form = ReviewForm(instance=user_review)

    return render(request, 'shop/product_detail.html', {
        'product':     product,
        'reviews':     reviews,
        'form':        form,
        'user_review': user_review,
    })

@login_required
def delete_review(request, pk):
    review     = get_object_or_404(Review, pk=pk, user=request.user)
    product_pk = review.product.pk
    review.delete()
    return redirect('product_detail', pk=product_pk)

@login_required
def vote_review(request, pk, vote_type):
    review = get_object_or_404(Review, pk=pk)
    if review.user == request.user:
        return redirect('product_detail', pk=review.product.pk)
    vote, created = ReviewVote.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'vote_type': vote_type}
    )
    if not created:
        vote.vote_type = vote_type
        vote.save()
    return redirect('product_detail', pk=review.product.pk)

@login_required
def report_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    ReviewReport.objects.get_or_create(review=review, user=request.user)
    return redirect('product_detail', pk=review.product.pk)

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items   = cart.items.select_related('product')
    return render(request, 'shop/cart.html', {'cart': cart, 'items': items})

@login_required
def add_to_cart(request, pk):
    product  = get_object_or_404(Product, pk=pk)
    cart, _  = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        item.quantity += quantity
        item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart, product_id=pk).delete()
    return redirect('cart')

def is_customer_service(user):
    return user.is_staff

@user_passes_test(is_customer_service)
def cs_portal(request):
    products         = Product.objects.all()
    reported_reviews = ReviewReport.objects.select_related(
        'review', 'review__product', 'user'
    )
    return render(request, 'shop/cs_portal.html', {
        'products':         products,
        'reported_reviews': reported_reviews,
    })

@user_passes_test(is_customer_service)
def cs_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cs_portal')
    else:
        form = ProductForm()
    return render(request, 'shop/cs_product_form.html', {'form': form, 'edit': False})

@user_passes_test(is_customer_service)
def cs_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('cs_portal')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/cs_product_form.html', {'form': form, 'edit': True})

@user_passes_test(is_customer_service)
def cs_deactivate_review(request, pk):
    review           = get_object_or_404(Review, pk=pk)
    review.is_active = False
    review.save()
    return redirect('cs_portal')

@user_passes_test(is_customer_service)
def cs_delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('cs_portal')