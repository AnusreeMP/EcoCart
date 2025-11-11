from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('blog', views.blog_page, name='blog'),
    path('blog/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('shop', views.shop, name='shop'),
    path('admin-panel/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:id>/', views.delete_category, name='delete_category'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('userhome/', views.userhome, name='userhome'),
    path('search/', views.search, name='search'),
    path('profile/', views.user_profile, name='user_profile'),
    path('orders/', views.user_orders, name='user_orders'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog-list/', views.blog_list, name='blog_list'),
    path('blog-detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('add-blog/', views.add_blog, name='add_blog'),
    path('edit-blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('productslist/', views.product_list, name='products'),
    path('category_page/', views.categories, name='category_page'),
    path('products/', views.products, name='products'),
    path('block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock-user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('delete-blog/<int:id>/', views.delete_blog, name='delete_blog'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
]





    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
