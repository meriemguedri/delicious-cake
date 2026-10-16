from django.urls import path
from . import views

urlpatterns = [
    path('',                             views.product_list,         name='home'),
    path('products/<int:pk>/',           views.product_detail,       name='product_detail'),
    path('reviews/<int:pk>/delete/',     views.delete_review,        name='delete_review'),
    path('reviews/<int:pk>/vote/<str:vote_type>/', views.vote_review,name='vote_review'),
    path('reviews/<int:pk>/report/',     views.report_review,        name='report_review'),
    path('cart/',                        views.cart_view,            name='cart'),
    path('cart/add/<int:pk>/',           views.add_to_cart,          name='add_to_cart'),
    path('cart/remove/<int:pk>/',        views.remove_from_cart,     name='remove_from_cart'),
    path('cs/',                          views.cs_portal,            name='cs_portal'),
    path('cs/add/',                      views.cs_add_product,       name='cs_add_product'),
    path('cs/edit/<int:pk>/',            views.cs_edit_product,      name='cs_edit_product'),
    path('cs/review/<int:pk>/deactivate/', views.cs_deactivate_review, name='cs_deactivate_review'),
    path('cs/review/<int:pk>/delete/',   views.cs_delete_review,     name='cs_delete_review'),
]