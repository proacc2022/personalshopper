from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.forms import inlineformset_factory

from .forms import *

# Create your views here.
from product.models import Category
from cart.models import *


@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    ty = current_user.id
    profile1 = User1Profile.objects.filter(user_id=ty)
    profile2 = User2Profile.objects.filter(user_id=ty)
    context = {'category': category,
               'profile1': profile1,
               'profile2': profile2}
    return render(request, 'user_profile.html', context)


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.warning(request, "Login Error! Username or Password is incorrect")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login_form.html', context)


@login_required(login_url='/login')  # Check login
def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')


def newsignup(request):
    if request.method == 'POST':
        form = SignUp1Form(request.POST)
        form1 = SignUp2Form(request.POST)
        form2 = SignUp3Form(request.POST)
        if form.is_valid() and form1.is_valid() and form2.is_valid():
            form.save()
            ok1 = form1.save(False)
            ok2 = form2.save(False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            ok1.user_id = current_user.id
            ok1.save()
            ok2.user_id = current_user.id
            ok2.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            messages.warning(request, form1.errors)
            messages.warning(request, form2.errors)
            return HttpResponseRedirect('/signup')

    form = SignUp1Form()
    form1 = SignUp2Form()
    form2 = SignUp3Form()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               'form1': form1,
               'form2': form2
               }
    return render(request, 'signup_form.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        context = {
            'category': category,
            'user_form': user_form,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def user_addressupdate(request):
    current_user = request.user  # Access User Session information
    ty = current_user.id
    pare = User.objects.get(pk=ty)
    chilFormset = inlineformset_factory(User, User1Profile, fields=('address', 'city', 'state', 'pin_code', 'country',),
                                        extra=1, )
    if request.method == 'POST':
        print("1")
        formset = chilFormset(request.POST, instance=pare)
        if formset.is_valid():
            formset.save()
            print("3")
            messages.success(request, 'Your account has been updated!')
            return redirect('index')
    print("2")
    category = Category.objects.all()
    formset = chilFormset(instance=pare)
    for form in formset:
        for fields in form:
            fields.field.widget.attrs['style'] = 'width:700px; height:25px;'
    context = {
        'category': category,
        'formset': formset
    }
    return render(request, 'user_addressupdate.html', context)


@login_required(login_url='/login')
def user_contactupdate(request):
    current_user = request.user  # Access User Session information
    ty = current_user.id
    print(ty)
    pare = User.objects.get(pk=ty)
    chilFormset = inlineformset_factory(User, User2Profile, fields=('phone',), extra=1, )
    if request.method == 'POST':
        formset = chilFormset(request.POST, instance=pare)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    category = Category.objects.all()
    formset = chilFormset(instance=pare)
    context = {
        'category': category,
        'formset': formset
    }
    return render(request, 'user_contactupdate.html', context)


@login_required(login_url='/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        # category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,  # 'category': category
                                                      })


@login_required(login_url='/login')  # Check login
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')  # Check login
def user_orderdetail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product(request):
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    profile1 = User1Profile.objects.filter(user_id=current_user.id)
    profile2 = User2Profile.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'order_product': order_product,
               'profile1': profile1,
               'profile2': profile2,
               }
    return render(request, 'user_order_products.html', context)


def password_reset_request(request):
    print("1111111111111111111111111111111111111111111111111111")
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    current_site = get_current_site(request)
                    c = {
                        "email": user.email,
                        'domain': current_site.domain,
                        'site_name': 'Personal Shopper',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'personalshopper.ibm@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
            else:
                return render(request, 'registration/NosuchEmail.html')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html",
                  context={"password_reset_form": password_reset_form})


def user_managepayment(request):
    return render(request=request, template_name="managepayment.html")


def ccuser_managepayment(request):
    current_user = request.user  # Access User Session information
    ty = current_user.id
    pare = User.objects.get(pk=ty)
    chilFormset = inlineformset_factory(User, User3Profile,
                                        fields=('ccardnumber', 'cexpmonth', 'cexpyear', 'cnameoncard', 'ccvv',),
                                        extra=1, )
    if request.method == 'POST':
        print("1")
        formset = chilFormset(request.POST, instance=pare)
        if formset.is_valid():
            formset.save()
            print("3")
            messages.success(request, 'Your account has been updated!')
            return redirect('index')
    print("2")
    category = Category.objects.all()
    formset = chilFormset(instance=pare)
    for form in formset:
        for fields in form:
            fields.field.widget.attrs['style'] = 'width:400px; height:25px;'
    context = {
        'category': category,
        'formset': formset
    }
    return render(request, 'user_creditcardupdate.html', context)


def dcuser_managepayment(request):
    current_user = request.user  # Access User Session information
    ty = current_user.id
    pare = User.objects.get(pk=ty)
    chilFormset = inlineformset_factory(User, User4Profile,
                                        fields=('dcardnumber', 'dexpmonth', 'dexpyear', 'dnameoncard', 'dcvv',),
                                        extra=1, )
    if request.method == 'POST':
        print("1")
        formset = chilFormset(request.POST, instance=pare)
        if formset.is_valid():
            formset.save()
            print("3")
            messages.success(request, 'Your account has been updated!')
            return redirect('index')
    print("2")
    category = Category.objects.all()
    formset = chilFormset(instance=pare)
    for form in formset:
        for fields in form:
            fields.field.widget.attrs['style'] = 'width:400px; height:25px;'
    context = {
        'category': category,
        'formset': formset
    }
    return render(request, 'user_debitcardupdate.html', context)


def user_upimanagepayment(request):
    current_user = request.user  # Access User Session information
    ty = current_user.id
    print(ty)
    pare = User.objects.get(pk=ty)
    chilFormset = inlineformset_factory(User, User5Profile, fields=('upiid',), extra=1, )
    if request.method == 'POST':
        formset = chilFormset(request.POST, instance=pare)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    category = Category.objects.all()
    formset = chilFormset(instance=pare)
    context = {
        'category': category,
        'formset': formset
    }
    return render(request, 'user_upiupdate.html', context)


def user_paytmmanagepayment(request):
    current_user = request.user  # Access User Session information
    ty = current_user.id
    print(ty)
    pare = User.objects.get(pk=ty)
    chilFormset = inlineformset_factory(User, User6Profile, fields=('paytmnumber',), extra=1, )
    if request.method == 'POST':
        formset = chilFormset(request.POST, instance=pare)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    category = Category.objects.all()
    formset = chilFormset(instance=pare)
    context = {
        'category': category,
        'formset': formset
    }
    return render(request, 'user_paytmupdate.html', context)
