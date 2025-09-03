from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from login_sigin.views import login_view
from home.models import Product,Imageset,cart,coments,Cate
from .models import orders
from login_sigin.models import usermodel
from datetime import timedelta,datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import random
from functools import wraps



def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_name'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

       



def mshoes_view(request,name=None):

    if name:
        products=Product.objects.filter(brand__name=name,gender__name='Male')
    else:
        products = Product.objects.filter(cat__name='Shoes',gender__name='Male')

    

    product_list = []
    for product in products:   # ✅ iterate each product
        # clean offer
        offer = int(str(product.offer).replace("%", "").strip())

        # clean price
        og_price = int(str(product.prce).replace(",", "").strip())

        # discounted price
        up_price = og_price - (offer * og_price // 100)

        product_list.append({
            "id": product.id,
            "name": product.name,
            "brand": getattr(product, "brand", None),
            "prce": product.prce,
            "offer": product.offer,
            "og_price": og_price,
            "up_price": up_price,
            "image_set": getattr(product, "image_set", None),
        })

    # delivery dates (same for all)
    day = random.randint(3, 6)
    today = datetime.today()
    delivery_date = today + timedelta(days=day)
    fst_delivery = today + timedelta(days=1)

    msg = f"Free delivery {delivery_date.strftime('%A, %d %B %Y')}"
    fst = f"Or Fast delivery {fst_delivery.strftime('%A, %d %B %Y')}"

    ns = request.session.get('user_name', None)
    
    if ns is None:
        user_nm='Login'
    else:
        user_nm=ns

    return render(request, 'mshoes.html', {
        'username': user_nm,
        "data": product_list,
        "time": msg,
        "fst": fst,
        

    })

'''
def show(request):
     
      products=Product.objects.filter(id=1)
      return render(request,'new.html',{'products':products})
'''
def show(request):
    products = Product.objects.all()
   

    ns = request.session.get('user_name', None)
    return render(request, 'new.html', {
        'username': ns,
        'products': products,
       

    })

'''
def product_list(request, no):

    products=Product.objects.filter(id=no)
    product = get_object_or_404(Product, id=no)  # single product
    imageset = Imageset.objects.get(id=no)

    # clean offer (remove % if stored like "7%")
    offer = int(product.offer.replace("%", ""))  

    # clean price (remove commas if stored like "10,000")
    og_price = int(product.prce.replace(",", ""))

    # discounted price
    up_price = og_price - (offer * og_price // 100)

    # delivery dates
    day = random.randint(3, 6)
    today = datetime.today()
    delivery_date = today + timedelta(days=day)
    fst_delivery = today + timedelta(days=1)

    msg = f"Free delivery in {day} days — {delivery_date.strftime('%A, %d %B %Y')}"
    fst = f"Or Fast delivery by Tomorrow, {fst_delivery.strftime('%A, %d %B %Y')}"
    ns = request.session.get('user_name', None)

      
    #cart
    if "quantity" in request.GET:
      user_model=usermodel.objects.filter(username=ns)
      size=request.GET.get('size')
      quantity = request.GET.get("quantity", 1)
      if ns is None:
          print()
          user_name='login'
      else:
        
        if request.method == 'POST':
      
           cmt=request.POST['text']
           coments.objects.create(
           no=no,
           user_name=ns,
           user_com=cmt
           )

    new_cart = cart.objects.create(
    user_name=ns,
        
    name=product.name,
    price=int(product.prce.replace(',', '')),
    quantity=quantity,
    no=no,
    size=size,
    image=product.image_set.img1
       )
    return redirect('cart')

   
  
    view_coments = coments.objects.filter(no=no)
    
    if ns is None:
        user_nm='Login'
    else:
        user_nm=ns
   
    
    return render(
        request,
        "about.html",
        {   'username': user_nm,
             'view_cmt':view_coments,
            "products": products,     # ✅ single object, not list
            "imageset": imageset,
            "time": msg,
            "fst": fst,
            "og_price": og_price,
            "up_price": up_price,
            
            
        },
    )
'''



def product_list(request, no):
    # Get product and related objects
    product = get_object_or_404(Product, id=no)
    products = Product.objects.filter(id=no)
    imageset = product.image_set  

    # Clean offer (remove % if stored like "7%")
    offer = int(product.offer.replace("%", "")) if product.offer else 0  

    # Clean price (remove commas if stored like "10,000")
    og_price = int(product.prce.replace(",", ""))  

    # Discounted price
    up_price = og_price - (offer * og_price // 100)

    # Delivery dates
    day = random.randint(3, 6)
    today = datetime.today()
    delivery_date = today + timedelta(days=day)
    fst_delivery = today + timedelta(days=1)

    msg = f"Free delivery in {day} days — {delivery_date.strftime('%A, %d %B %Y')}"
    fst = f"Or Fast delivery by Tomorrow, {fst_delivery.strftime('%A, %d %B %Y')}"

    # Session username
    ns = request.session.get('user_name', None)

    # ✅ Handle Add to Cart
    if "quantity" in request.GET:
        size = request.GET.get('size')
        quantity = int(request.GET.get("quantity", 1))


        cart.objects.create(
            user_name=ns,
            name=product.name,
            price=og_price,
            quantity=quantity,
            no=no,
            size=size,
            image=product.image_set.img1 if product.image_set else None
        )
        return redirect('cart')

    # ✅ Handle Comments (only logged in users)
    if request.method == 'POST':
        if ns is None:  # not logged in
            return redirect('login')  # send to login page
        else:
            cmt = request.POST.get('text')
            if cmt:
                coments.objects.create(
                    no=no,
                    user_name=ns,
                    user_com=cmt
                )
            return redirect('product_list', no=no)

    # Get all comments
    view_coments = coments.objects.filter(no=no)

    # Username display
    user_nm = ns if ns else 'Login'

    return render(
        request,
        "about.html",
        {
            'username': user_nm,
            'view_cmt': view_coments,
            "products": products,     
            "product": product,       
            "imageset": imageset,
            "time": msg,
            "fst": fst,
            "og_price": og_price,
            "up_price": up_price,
        },
    )

'''
@custom_login_required
def brand_view(request):
    random_num=random.randint(999,10000)
    ns = request.session.get('user_name', None)
    
    print(ns)
    

    boolen=True

    while boolen:
       if orders.ord_no == random_num:
           random_num=random.randint(999,10000)
           request.session['ordno']=random_num
           print('number',request.session.get('ordno'))
          
  
       else:
           
           boolen=False

         # order object
    am=request.POST.get('gtotal')
    orders.objects.create(
          ord_no=random_num,
          u_name=ns,
          amount=am,
          state='pending..'
       
          )
    

    
    
   
           # Replace with your actual details
    upi_id = "sasikirand@ybl"
    name = "sasi"
    amount = am
    note = random_num

    upi_url = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn={note}"

    context = {
             "upi_url": upi_url,
              "upi_id": upi_id,
              "name": name,
              "amount": am,
              "note": random_num,
             }
         


           
    return render(request, "view.html", context)
    
   '''

@custom_login_required
def brand_view(request):
    ns = request.session.get('user_name', None)

    # Generate unique random order number
    random_num = random.randint(999, 10000)
    while orders.objects.filter(ord_no=random_num).exists():
        random_num = random.randint(999, 10000)

    # Save to session
    request.session['ordno'] = random_num
    print("Order number saved in session:", request.session.get('ordno'))

    # Get amount
    am = request.POST.get('gtotal')

    # Create order
    orders.objects.create(
        ord_no=random_num,
        u_name=ns,
        amount=am,
        state='pending..'
    )

    # Payment details
    upi_id = "7075638319@axl"
    name= "Sai datt"
    amount = am
    note = random_num   # using order number as note

    upi_url = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn={note}"

    context = {
        "upi_url": upi_url,
        "upi_id": upi_id,
        "name": name,
        "amount": am,
        "note": random_num,
    }
   
   # return render(request, "view.html", context,{'data':am})
    return render(request, "view.html", {
    "upi_url": upi_url,
    "upi_id": upi_id,
    "name": name,
    "amount": am,
    "note": random_num,
    "data": am
    })


def cart_view(request):
   
    
    ns = request.session.get('user_name', None)
    user_model=usermodel.objects.filter(username=ns)
    card_db=cart.objects.filter(user_name=ns)

    
    if ns is None:
        user_nm='Login'
    else:
        user_nm=ns

    print(user_nm)
    
    
   
    return render(request,'cart.html',{'data':card_db, 'username': user_nm})

def del_cart(request,num):
   # cart_del=get_object_or_404(cart, no=num) 
    cart_del=cart.objects.filter(no=num)

    cart_del.delete()
    return redirect('cart')

def logout_view(request):
    logout(request)
    
    return redirect('home')

@login_required
def status(request):
    ns = request.session.get('user_name', None)
    cart_db=cart.objects.filter(user_name=ns)
    order_db = orders.objects.filter(u_name=ns).first()
    #order_db=get_object_or_404(orders,u_name=ns)
     
    if ns is None:
        user_nm='Login'
    else:
        user_nm=ns

    print(user_nm)
    
       

    return render(request,'status.html',{'data':cart_db,'ord':order_db,'username': user_nm})
def payment(request):
    ns = request.session.get('user_name', None)
    print('oreno',request.session.get('ordno'))
    rm = request.session.get('ordno')

    if not rm:
        return redirect('cart')

    try:
        order_db = orders.objects.get(ord_no=rm, u_name=ns)  # check user too
        order_db.delete()
        # Optionally clear session
        del request.session['ordno']
        return redirect('home')
    except orders.DoesNotExist:
        return redirect('home')









    

