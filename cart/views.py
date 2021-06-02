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
            else:  # Insert to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                leftover = product.product_stock - form.cleaned_data['quantity']
                if leftover >= 0:
                    data.quantity = form.cleaned_data['quantity']
                    data.save()

        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            quantity_desired = data.quantity + 1
            leftover = product.product_stock - quantity_desired
            if leftover >= 0:
                data.quantity += 1
                data.save()
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            leftover = product.product_stock - 1
            if leftover >= 0:
                data.quantity = 1
                data.save()  #
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
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')  # Check login
def addproduct(request, id):
    current_user = request.user  # Access User Session information
    # product = Product.objects.get(pk=id)
    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
    data.quantity += 1
    data.save()  #

    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')  # Check login
def reduceproduct(request, id1, id2):
    current_user = request.user  # Access User Session information
    # product = Product.objects.get(pk=id1)
    data = ShopCart.objects.get(product_id=id1, user_id=current_user.id)
    data.quantity -= 1
    data.save()
    if data.quantity == 0:
        ShopCart.objects.filter(id=id2).delete()
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
        if request.POST.get("form_type") == 'formOne':
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
                # return render(request, 'Order_Completed.html',{'ordercode':ordercode,'category': category})
                return HttpResponseRedirect(reverse("ordercompleted"))
            else:
                print(form.errors)
                if str(form.errors).find(
                        '<li>paymethodselection<ul class="errorlist"><li>This field is required.</li></ul></li>') > 0:
                    messages.warning(request, 'There are no payment details added. Please add a payment method.')
                    print('hhhhhhhhhhhhhhhhhhhhhhlllllllllllllllllllllllllllll')
                    print(form.errors)
                    return HttpResponseRedirect(reverse("orderproduct"))
                return HttpResponseRedirect(reverse("orderproduct"))
        elif request.POST.get("form_type") == 'formTwo':
            cform = addcreditcard(request.POST)
            print(cform)
            if cform.is_valid():
                ok = cform.save(False)
                ok.user_id = current_user.id
                ok.save()
                return HttpResponseRedirect(reverse("orderproduct"))
            else:
                print(cform.errors)
                return HttpResponseRedirect(reverse("/cart/orderproduct"))
        elif request.POST.get("form_type") == 'formThree':
            dform = adddebitcard(request.POST)
            print(dform)
            if dform.is_valid():
                ok = dform.save(False)
                ok.user_id = current_user.id
                ok.save()
                return HttpResponseRedirect(reverse("orderproduct"))
            else:
                print(dform.errors)
                return HttpResponseRedirect(reverse("/cart/orderproduct"))
        elif request.POST.get("form_type") == 'formFour':
            upform = addupiid(request.POST)
            print(upform)
            if upform.is_valid():
                ok = upform.save(False)
                ok.user_id = current_user.id
                ok.save()
                return HttpResponseRedirect(reverse("orderproduct"))
            else:
                print(upform.errors)
                return HttpResponseRedirect(reverse("/cart/orderproduct"))
        elif request.POST.get("form_type") == 'formFive':
            payform = addpaytmno(request.POST)
            print(payform)
            if payform.is_valid():
                ok = payform.save(False)
                ok.user_id = current_user.id
                ok.save()
                return HttpResponseRedirect(reverse("orderproduct"))
            else:
                print(payform.errors)
                return HttpResponseRedirect(reverse("/cart/orderproduct"))
    if count3 < 1 and count1 > 0 and count2 > 0:
        return HttpResponseRedirect("/shopcart/")
    elif count1 > 0 and count2 > 0:
        tform.fields['addoptionselection'].queryset = User1Profile.objects.filter(user_id=current_user.id)
        tform.fields['phoneoptionselection'].queryset = User2Profile.objects.filter(user_id=current_user.id)
        # tform.fields['addoptionselection'].to_field_name = "id"
        tform.fields['addoptionselection'].widget.attrs['style'] = 'width:300px; height:25px;'
        print(tform.fields['paymethodselection'].choices)
        tform.fields['paymethodselection'].choices = choices_list
        print(tform.fields['paymethodselection'].choices)
        profile1 = User1Profile.objects.filter(user_id=current_user.id)
        profile2 = User2Profile.objects.filter(user_id=current_user.id)
        ccform = addcreditcard()
        ddform = adddebitcard()
        upiform = addupiid()
        paytmform = addpaytmno()
        context = {'shopcart': shopcart,
                   'category': category,
                   'total': total,
                   'form': tform,
                   'profile1': profile1,
                   'profile2': profile2,
                   'count3': count3,
                   'ccform': ccform,
                   'ddform': ddform,
                   'upiform': upiform,
                   'paytmform': paytmform,
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


def ok404(request, exception=None):
    category = Category.objects.all()
    return render(request, '404.html', {'category': category})

def ok500(request, exception=None):
    category = Category.objects.all()
    return render(request, '500.html', {'category': category})