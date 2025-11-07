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

   
   


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
