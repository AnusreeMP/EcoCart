from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Blog
from django.shortcuts import render, get_object_or_404
from .models import Product,Category,CustomUser
from django.contrib.auth import get_user_model



# Create your views here.
def index(request):
    # items = Product.objects.all()[:8]
    items = []  # temporary placeholder
    return render(request, 'index.html', {'items': items})

User = get_user_model()
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            address=address,
            pincode=pincode
        )
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'registration.html')



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('userhome')  # You can change this to your home page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You’ve been logged out successfully.")
    return redirect('login')


def blog_page(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request, 'blog.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def shop(request):
    products = Product.objects.all().order_by('id')
    return render(request, 'shop.html', {'products': products})


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or not authorized'})
    
    return render(request, 'admin_login.html')

def admin_dashboard(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'admin_dashboard.html', {
        'products': products,
        'categories': categories,
        'users': users
    })

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category_id = request.POST['category']
        image = request.FILES.get('image')

        category = Category.objects.get(id=category_id)
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image
        )
        messages.success(request, "Product added successfully!")
        return redirect('admin_dashboard')

    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})


def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.category_id = request.POST['category']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('admin_dashboard')

    categories = Category.objects.all()
    return render(request, 'edit_product.html', {'product': product, 'categories': categories})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('admin_dashboard')


def manage_categories(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect('manage_categories')

    categories = Category.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('manage_categories')
    return render(request, 'add_category.html')
def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('manage_categories')
    return render(request, 'edit_category.html', {'category': category})

def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('manage_categories')
   


def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'manage_users.html', {'users': users})

def userhome(request):
    return render(request, 'userhome.html')


def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})


def user_profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})















