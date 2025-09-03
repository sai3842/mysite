from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from login_sigin.views import login_view
from home.models import Product,Imageset,cart,coments
from login_sigin.models import usermodel
from datetime import timedelta,datetime
import random


def msandles(request,name=None):

    if name:
        products=Product.objects.filter(brand__name=name)
    else:
        products = Product.objects.filter(cat__name='Sandles',gender__name='Male')

    

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

    return render(request, 'msandles.html', {
        'username': user_nm,
        "data": product_list,
        "time": msg,
        "fst": fst,
    })
