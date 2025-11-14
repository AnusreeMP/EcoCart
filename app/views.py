from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from .models import Product,Category,CustomUser,Blog
from django.contrib.auth import get_user_model
from .models import  Cart,Order,OrderItem,Wishlist
from django.contrib.auth.decorators import user_passes_test




# Create your views here.
def index(request):
    items = [] 
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
            # ✅ Block admin users from logging in through this page
            if user.is_superuser or user.is_staff:
                messages.error(request, "Admins must log in from the admin panel.")
                return redirect('login')

            # ✅ Normal user login
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('userhome')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You’ve been logged out successfully.")
    return redirect('login')

def add_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        Blog.objects.create(title=title, content=content, image=image)
        messages.success(request, "Blog added successfully!")
        return redirect('admin_dashboard')
    return render(request, 'add_blog.html')


def admin_view_blog(request):
    blogs = Blog.objects.all()
    return render(request, 'admin_view_blog.html', {'blogs': blogs})

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        blog.save()
        messages.success(request, "Blog updated successfully!")
        return redirect('admin_dashboard')
    return render(request, 'edit_blog.html', {'blog': blog})

def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, "Blog deleted successfully!")
    return redirect('admin_dashboard')

def blog_list(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request, 'blog_list.html', {'blogs': blogs})



def blog_page(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request, 'blog.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def change_cart(request, product_id):
    
    if request.method == "POST":
        action = request.POST.get("action")
        product = get_object_or_404(Product, id=product_id)
        cart_item = Cart.objects.filter(user=request.user, product=product).first()

        if not cart_item:
            return redirect('cart')

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()

        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        elif action == "remove":
            cart_item.delete()

    return redirect('cart')



def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart.objects.filter(user=request.user, product=product).delete()
    return redirect('cart')


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.total_price for item in cart_items)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total_amount": total_amount,
    })


def place_order(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        address_order = request.POST.get("address")
        print( "Address:", address_order)  # Debugging line

        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect("checkout")

        # Create Order
        order = Order.objects.create(
            user=request.user,
            address_order=address_order,
            payment_method=payment_method,  # Temporary
        )

        # Save Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # -------- PAYMENT HANDLING -------- #
        payment = request.POST.get("payment_method")

        if payment == "COD":
            order.payment_method = "Cash on Delivery"

        elif payment == "UPI":
            upi_id = request.POST.get("upi_id")
            order.payment_method = f"UPI - {upi_id}"

        elif payment == "CARD":
            card_number = request.POST.get("card_number")
            expiry = request.POST.get("expiry")
            cvv = request.POST.get("cvv")
            safe_number = card_number[-4:] if card_number else "XXXX"
            order.payment_method = f"Card Ending With {safe_number}"

        order.save()

        # Clear cart after ordering
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect("order_success", order_id=order.id)


    return redirect("checkout")

def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    items = order.items.all()

    return render(request, "order_success.html", {"order": order, "items": items})

def edit_address(request):
    if request.method == "POST":
        new_address = request.POST.get("address")
        user = request.user
        user.address = new_address
        user.save()
        messages.success(request, "Address updated successfully!")
        return redirect("checkout")
    return render(request, "edit-address.html")





def update_cart(request, item_id):
    if request.method == "POST":
        action = request.POST.get("action")
        cart_item = Cart.objects.get(id=item_id, user=request.user)

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
    return redirect('checkout')

def payment_page(request):
    return render(request, 'payment.html')

def mock_payment_success(request):
    if request.method == 'POST':
        return render(request, 'payment_success.html')
    return render(request,'payment.html')
    return redirect ('userhome')






def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Order.objects.create(
        user=request.user,
        product_name=product.name,
        quantity=1,
        total_price=product.price,
    )
    return render(request, 'order_success.html')



def categories(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})

def products(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        print("Username:", username)  # Debugging line
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print("Authenticated User:", user)  # Debugging line

        if user is not None and user.is_staff:
            print("Admin login successful")  # Debugging line
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or not authorized'})
    
    return render(request, 'admin_login.html')




def admin_dashboard(request):
    if request.user.is_staff:
        
        context = {
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
            'blogs': Blog.objects.all(),
            'users': CustomUser.objects.all(),
        }
        return render(request, 'admin_dashboard.html', context)
    return redirect('admin_login')

def admin_view_products(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'adminviewproducts.html', {'products': products})

def admin_manage_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, "admin_manage_orders.html", {"orders": orders})


def update_order_status(request, order_id):
    if request.method == "POST":
        new_status = request.POST.get("status")
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
        messages.success(request, "Order status updated successfully!")
        return redirect("admin_manage_orders")

 

def block_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_dashboard')

def unblock_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_dashboard')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')

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


def edit_product(request,  product_id):
    product = get_object_or_404(Product, id=product_id)
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
    products = Product.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('query')
    category = request.GET.get('category')
    user_wishlist = []
    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__name=category)
    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product__name', flat=True)

    return render(request, 'userhome.html', {
        'products': products,
        'categories': categories,
        'user_wishlist': user_wishlist
    })



def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)
    return render(request, 'userhome.html', {'products': products, 'query': query})


def user_profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})

def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, "user_orders.html", {"orders": orders})



def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})
 
def wishlist(request):
    sort_by = request.GET.get('sort', 'newest')
    items = Wishlist.objects.filter(user=request.user)
    if sort_by == 'price_low_to_high':
        items = items.order_by('price')
    elif sort_by == 'price_high_to_low':
        items = items.order_by('-price')
    else:  
        items = items.order_by('-date_added')

    # 🪄 Optional: show message if wishlist is empty
    if not items.exists():
        messages.info(request, "Your wishlist is empty 🌿")

    # 🎨 Render template
    return render(request, 'wishlist.html', {
        'items': items,
        'sort_by': sort_by
    })

def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    # Check if this product is already in the wishlist for this user
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={
            'product_name': product.name,
            'product_image': product.image,
            'price': product.price
        }
    )

    if created:
        messages.success(request, f"✅ '{product.name}' added to your wishlist!")
    else:
        messages.info(request, f"❤️ '{product.name}' is already in your wishlist.")

    return redirect('wishlist')

def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist.delete()
    return redirect('wishlist')


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

















