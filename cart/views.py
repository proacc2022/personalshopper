from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from cart.models import *
from product.models import Category, Product
from .forms import *


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)

    checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id)  # Check product in shopcart
    if checkinproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                quantity_desired = data.quantity + form.cleaned_data['quantity']
                leftover = product.product_stock - quantity_desired
                if leftover >= 0:
                    data.quantity += form.cleaned_data['quantity']
                    data.save()  # save data
                    messages.success(request, "Product added to Shopcart ")
                else:
                    messages.info(request, "Out of Stock. Decrease your quantity and try.")
            else:  # Insert to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                leftover = product.product_stock - form.cleaned_data['quantity']
                if leftover >= 0:
                    data.quantity = form.cleaned_data['quantity']
                    data.save()
                    messages.success(request, "Product added to Shopcart ")
                else:
                    messages.info(request, "Out of Stock. Decrease your quantity and try.")

        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            quantity_desired = data.quantity + 1
            leftover = product.product_stock - quantity_desired
            if leftover >= 0:
                data.quantity += 1
                data.save()
                messages.success(request, "1 item added to Shopcart ")
            else:
                messages.info(request, "Out of stock. Cannot add item")
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            leftover = product.product_stock - 1
            if leftover >= 0:
                data.quantity = 1
                data.save()  #
                messages.success(request, "Product added to Shopcart ")
            else:
                messages.info(request, "Out of Stock.")
        return HttpResponseRedirect(url)


@login_required(login_url='/login')  # Check login
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart1 = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart1:
        if rs.quantity > rs.product.product_stock:
            if rs.product.product_stock > 0:
                rs.quantity = rs.product.product_stock
            else:
                rs.delete()
        total += rs.product.product_discount * rs.quantity
        rs.save()
    # return HttpResponse(str(total))
    context = {'shopcart': shopcart1,
               'category': category,
               'total': total,
               }
    return render(request, 'shopcart_products.html', context)


@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')  # Check login
def addproduct(request, id):
    current_user = request.user  # Access User Session information
    #product = Product.objects.get(pk=id)
    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
    data.quantity += 1
    data.save()  #

    messages.success(request, "Product added to Shopcart")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')  # Check login
def reduceproduct(request, id1, id2):
    current_user = request.user  # Access User Session information
    #product = Product.objects.get(pk=id1)
    data = ShopCart.objects.get(product_id=id1, user_id=current_user.id)
    data.quantity -= 1
    data.save()
    if data.quantity == 0:
        ShopCart.objects.filter(id=id2).delete()
        messages.success(request, "Your item deleted form Shopcart.")
    else:
        messages.success(request, "Product reduced from Shopcart")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')  # Check login
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.product_discount * rs.quantity
    tform = OrderForm()
    count1 = User1Profile.objects.filter(user_id=current_user.id).count()
    count2 = User2Profile.objects.filter(user_id=current_user.id).count()
    print(count1)
    print(count2)
    print(current_user.id)
    count3 = shopcart.count()
    print(count3)
    choices_list = []
    ki1 = User3Profile.objects.values_list('ccardnumber', flat=True).filter(user_id=current_user.id)
    ki2 = User4Profile.objects.values_list('dcardnumber', flat=True).filter(user_id=current_user.id)
    ki3 = User5Profile.objects.values_list('upiid', flat=True).filter(user_id=current_user.id)
    ki4 = User6Profile.objects.values_list('paytmnumber', flat=True).filter(user_id=current_user.id)
    count4 = ki1.count()
    count5 = ki2.count()
    count6 = ki3.count()
    count7 = ki4.count()
    m = 1
    n = 1
    o = 1
    p = 1
    for i in ki1:
        choices_list.append(('CREDIT CARD ' + str(m), "".join(['*' for x in i[:-4]]) + i[-4:]))
        m = m + 1
    for j in ki2:
        choices_list.append(('DEBIT CARD ' + str(n), "".join(['*' for x in j[:-4]]) + j[-4:]))
        n = n + 1
    for k in ki3:
        choices_list.append(('UPI ID ' + str(o), 'UPI ID ' + str(k)))
        o = o + 1
    for ll in ki4:
        choices_list.append(('PAYTM ' + str(p), 'PAYTM ' + str(ll)))
        p = p + 1
    print(choices_list)

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        print(form.fields['paymethodselection'].choices)
        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        form.fields['paymethodselection'].choices = choices_list
        print(form.fields['paymethodselection'].choices)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
            data = Order()
            selection = form.data['addoptionselection']
            selection2 = form.data['phoneoptionselection']
            print(selection)
            print(selection2)
            data.first_name = current_user.first_name
            data.last_name = current_user.last_name
            data.address = User1Profile.objects.values_list('address', flat=True).get(id=selection)
            data.city = User1Profile.objects.values_list('city', flat=True).get(id=selection)
            data.pin_code = User1Profile.objects.values_list('pin_code', flat=True).get(id=selection)
            data.state = User1Profile.objects.values_list('state', flat=True).get(id=selection)
            data.country = User1Profile.objects.values_list('country', flat=True).get(id=selection)
            data.phone = User2Profile.objects.values_list('phone', flat=True).get(id=selection2)
            data.user_id = current_user.id
            data.delivery_type = form.data['deloptionselection']
            print(total)
            if data.delivery_type == "Express Delivery":
                data.delivery_charge = 10
            else:
                data.delivery_charge = 0
            total = total + data.delivery_charge
            data.paymentmethod = form.cleaned_data['paymethodselection']
            data.total = total
            print(total)
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            data.code = ordercode
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.product_discount
                asf = rs.product.product_discount * rs.quantity
                detail.amount = asf
                detail.save()
                product = Product.objects.get(id=rs.product_id)
                product.product_stock -= rs.quantity
                product.save()
                # ************ <> *****************

            ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank you ")
            # return render(request, 'Order_Completed.html',{'ordercode':ordercode,'category': category})
            return HttpResponseRedirect(reverse("ordercompleted"))
        else:
            messages.warning(request, form.errors)
            print(form.errors)
            return HttpResponseRedirect(reverse("/cart/orderproduct"))

    if count3 < 1 and count1 > 0 and count2 > 0:
        return HttpResponseRedirect("/shopcart/")
    elif count1 > 0 and count2 > 0 and (count7 > 0 or count6 > 0 or count5 > 0 or count4 > 0):
        tform.fields['addoptionselection'].queryset = User1Profile.objects.filter(user_id=current_user.id)
        tform.fields['phoneoptionselection'].queryset = User2Profile.objects.filter(user_id=current_user.id)
        # tform.fields['addoptionselection'].to_field_name = "id"
        tform.fields['addoptionselection'].widget.attrs['style'] = 'width:300px; height:25px;'
        print(tform.fields['paymethodselection'].choices)
        tform.fields['paymethodselection'].choices = choices_list
        print(tform.fields['paymethodselection'].choices)
        profile1 = User1Profile.objects.filter(user_id=current_user.id)
        profile2 = User2Profile.objects.filter(user_id=current_user.id)
        context = {'shopcart': shopcart,
                   'category': category,
                   'total': total,
                   'form': tform,
                   'profile1': profile1,
                   'profile2': profile2,
                   'count3': count3,
                   }
        return render(request, 'Order_Form.html', context)
    else:
        context = {
            'category': category,
        }
        return render(request, 'Enter Address or Contact.html', context)


@login_required(login_url='/login')  # Check login
def ordercompleted(request):
    category = Category.objects.all()
    return render(request, 'Order_Completed.html', {'category': category})
