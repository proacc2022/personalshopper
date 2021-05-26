from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseRedirect
from home.forms import SearchForm
from django.http import HttpResponse
from django.shortcuts import render
from product.models import Category, Product, Images
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from urllib.parse import unquote


def index(request):
    category = Category.objects.all()
    sliderProducts = Product.objects.all().order_by('id')[:4]
    latestProducts = Product.objects.all().order_by('-id')[:4]
    randomProducts = Product.objects.all().order_by('?')[:4]
    page = 'home'
    context = {'page': page,
               'category': category,
               'sliderProducts': sliderProducts,
               'latestProducts': latestProducts,
               'randomProducts': randomProducts}
    return render(request, 'index.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    context = {'category': category,
               'product': product,
               'images': images,
               }
    return render(request, 'product_detail.html', context)


def category_products(request, id, slug):
    catdata = Category.objects.get(pk=id)
    category = Category.objects.all()
    all_prods = Product.objects.filter(category=id)
    if all_prods.count() > 0:
        page = request.GET.get('page', 1)
        paginator = Paginator(all_prods, 2)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
    else:
        products = Product.objects.filter(category=id)
    context = {'category': category,
               'catdata': catdata,
               'product': products,
               }
    # return HttpResponse(products)
    return render(request, 'category_products.html', context)


def search(request):
    print("huuuuuuuuuuuuuuwachii")
    if request.method == 'POST':
        print("iiiiiiiiiiiiiiiiiiiiiiiiiiiihuuuuuuuuuuuuuuwachii")
        form = SearchForm(request.POST)
        print("dddddddddddddddddddddddddddiiiiiiiiiiiiiiiiiiiiiiiiiiiihuuuuuuuuuuuuuuwachii")
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            print(query)
            if catid == 0:
                all_prods = Product.objects.filter(product_name__icontains=query)
            else:
                all_prods = Product.objects.filter(product_name__icontains=query, category=catid)
            print(all_prods)
            if all_prods.count() > 0:
                page = request.GET.get('page', 1)
                paginator = Paginator(all_prods, 2)
                try:
                    products = paginator.page(page)
                except PageNotAnInteger:
                    products = paginator.page(1)
                except EmptyPage:
                    products = paginator.page(paginator.num_pages)
            else:
                products = Product.objects.filter(category=catid)
            print(products)
            p = list(products)
            print(p)
            category = Category.objects.all()
            context = {
                'product': products,
                'category': category,
                'query': query,
                'catid': catid,
            }

            return render(request, 'search_product.html', context)
    elif request.method == "GET":
        print("Sarvesh")
        query = request.GET.get('que', 2)
        print(query)
        catid = request.GET.get('cid', 3)
        catid = int(catid)
        print(catid)
        print(type(catid))
        if catid == 0:
            all_prods = Product.objects.filter(product_name__icontains=query)
            print("ok")
        else:
            all_prods = Product.objects.filter(product_name__icontains=query, category=catid)
            print("notok")
        print(all_prods)
        if all_prods.count() > 0:
            page = request.GET.get('page', 1)
            paginator = Paginator(all_prods, 2)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
        else:
            products = Product.objects.filter(category=catid)
        print(products)
        p = list(products)
        print(p)
        category = Category.objects.all()
        context = {
            'product': products,
            'category': category,
            'query': query,
            'catid': catid,
        }
        return render(request, 'search_product.html', context)

    return HttpResponseRedirect('/')


chatbot = ChatBot('PSBot',
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter"
                  )

# Create a new trainer for the chatbot
trainer1 = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer1.train("chatterbot.corpus.english")

# Train based on the english corpus

# Already trained and it's supposed to be persistent
# chatbot.train("chatterbot.corpus.english")

trainer = ListTrainer(chatbot)

trainer.train([
    "Who made personal shopper website",
    "Sarvesh Agrawal and Abbas Savliwala",
])


@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')

        data = unquote(data)
        data = data[4:]
        if data.find('+') > -1:
            data = data.replace("+", " ")
        print(data)
        if data.find('in ') == 0 and data.find(' and ') > -1 and data.find(' product:') > -1 and data.find(
                ' brand:') > -1:
            try:
                test_sub1 = "in "
                stindex1 = [i for i in range(len(data)) if data.startswith(test_sub1, i)]
                print(stindex1)
                stindexf1 = []
                for i in stindex1:
                    try:
                        int(data[i + 3])
                        print("uhuhuh")
                        print(data[i + 3])
                        stindexf1.append(i + 3)
                    except:
                        pass
                print(stindexf1)
                test_sub2 = " and "
                stindex2 = [i for i in range(len(data)) if data.startswith(test_sub2, i)]
                print(stindex2)
                stindexf2 = []
                for i in stindex2:
                    try:
                        int(data[i + 5])
                        print("uhuhuh")
                        print(data[i + 5])
                        stindexf2.append(i + 5)
                    except:
                        pass
                print(stindexf2)
                for i in stindexf2:
                    if stindexf1[0] > i:
                        stindexf2.remove(i)
                for i in stindexf1:
                    if stindexf2[-1] < i:
                        stindexf1.remove(i)
                print(stindexf2)
                print(stindexf1)
                numb1 = ''
                numb2 = ''
                for i in data[int(stindexf1[0]):int(data[stindexf1[0]:].find(' ')) + int(stindexf1[0])]:
                    if i.isdigit():
                        numb1 = numb1 + i
                print(numb1)
                for i in data[int(stindexf2[0]):int(data[stindexf2[0]:].find(' ')) + int(stindexf2[0])]:
                    if i.isdigit():
                        numb2 = numb2 + i
                print(numb2)
                test_sub3 = " product:"
                stindex3 = [i for i in range(len(data)) if data.startswith(test_sub3, i)]
                print(stindex3)
                stindexf3 = []
                for i in stindex3:
                    try:
                        print("uhuhuh")
                        print(data[i + 9])
                        stindexf3.append(i + 9)
                    except:
                        pass
                print(stindexf3)
                data3 = data[int(stindexf3[0]):]
                print(data3)
                test_sub4 = " brand:"
                stindex4 = [i for i in range(len(data)) if data.startswith(test_sub4, i)]
                print(stindex4)
                stindexf4 = []
                for i in stindex4:
                    try:
                        print("uhuhuh")
                        print(data[i + 7])
                        stindexf4.append(i + 7)
                    except:
                        pass
                print(stindexf4)
                data4 = data[int(stindexf4[0]):int(stindex3[0])]
                print(data4)
                products_i = Product.objects.filter(product_name__icontains=data, product_brand__icontains=data4,
                                                    product_discount__gte=int(numb1),
                                                    product_discount__lte=int(numb2))
                print(products_i.count())
                datalt = data3.split(' ')
                print(datalt)
                x = len(datalt)
                print(x)
                prod = []
                for i in datalt:
                    products_k = Product.objects.filter(product_keywords__icontains=i, product_brand__icontains=data4,
                                                        product_discount__gte=int(numb1),
                                                        product_discount__lte=int(numb2))
                    prod.append(Product.objects.filter(product_keywords__icontains=i, product_brand__icontains=data4,
                                                       product_discount__gte=int(numb1),
                                                       product_discount__lte=int(numb2)))
                    print(products_k.count())
                do = 0
                for i in prod:
                    if do == 0:
                        products = i
                    else:
                        products = products.intersection(i)
                    do = do + 1
                products = products_i.union(products)
                if products.count() > 0:
                    st = ' '
                    if products.count() > 0:
                        st = 'Products found- <br> '
                    for product in products:
                        st = str(st) + " <br> " + str(
                            product.product_name) + " <br> " + "https:/" + "/personal-shopper-website.herokuapp.com/product/" + str(
                            product.id) + "/" + str(product.slug) + " <br> "
                    print(st)
                    chat_response = st
                    print(chat_response)
                else:
                    chat_response = "No product available with these specifications."
            except:
                chat_response = chatbot.get_response(data).text
        elif data.find('in ') == 0 and data.find(' and ') > -1 and data.find(' product:') > -1:
            try:
                test_sub = "in "
                stindex = [i for i in range(len(data)) if data.startswith(test_sub, i)]
                print(stindex)
                stindexf = []
                for i in stindex:
                    try:
                        int(data[i + 3])
                        print("uhuhuh")
                        print(data[i + 3])
                        stindexf.append(i + 3)
                    except:
                        pass
                print(stindexf)
                test_sub2 = " and "
                stindex2 = [i for i in range(len(data)) if data.startswith(test_sub2, i)]
                print(stindex2)
                stindexf2 = []
                for i in stindex2:
                    try:
                        int(data[i + 5])
                        print("uhuhuh")
                        print(data[i + 5])
                        stindexf2.append(i + 5)
                    except:
                        pass
                print(stindexf2)
                for i in stindexf2:
                    if stindexf[0] > i:
                        stindexf2.remove(i)
                for i in stindexf:
                    if stindexf2[-1] < i:
                        stindexf.remove(i)
                print(stindexf2)
                print(stindexf)
                numb1 = ''
                numb2 = ''
                for i in data[int(stindexf[0]):int(data[stindexf[0]:].find(' ')) + int(stindexf[0])]:
                    if i.isdigit():
                        numb1 = numb1 + i
                print(numb1)
                for i in data[int(stindexf2[0]):int(data[stindexf2[0]:].find(' ')) + int(stindexf2[0])]:
                    if i.isdigit():
                        numb2 = numb2 + i
                print(numb2)
                test_sub = " product:"
                stindex = [i for i in range(len(data)) if data.startswith(test_sub, i)]
                print(stindex)
                stindexf = []
                for i in stindex:
                    try:
                        print("uhuhuh")
                        print(data[i + 9])
                        stindexf.append(i + 9)
                    except:
                        pass
                print(stindexf)
                data = data[int(stindexf[0]):]
                print(data)
                products_i = Product.objects.filter(product_name__icontains=data, product_discount__gte=int(numb1),
                                                    product_discount__lte=int(numb2))
                print(products_i.count())
                datalt = data.split(' ')
                print(datalt)
                x = len(datalt)
                print(x)
                prod = []
                for i in datalt:
                    products_k = Product.objects.filter(product_keywords__icontains=i, product_discount__gte=int(numb1),
                                                        product_discount__lte=int(numb2))
                    prod.append(Product.objects.filter(product_keywords__icontains=i, product_discount__gte=int(numb1),
                                                       product_discount__lte=int(numb2)))
                    print(products_k.count())
                do = 0
                for i in prod:
                    if do == 0:
                        products = i
                    else:
                        products = products.intersection(i)
                    do = do + 1
                products = products_i.union(products)
                try:
                    catgoryids = Category.objects.values_list('id', flat=True).get(category_name__icontains=data)
                    products2 = Product.objects.filter(category_id=catgoryids, product_discount__gte=int(numb1),
                                                       product_discount__lte=int(numb2))
                    print(products2.count())

                except:
                    products2 = Product.objects.none()
                if products.count() > 0 or products2.count() > 0:
                    st = ' '
                    if products2.count() > 0:
                        st = 'Categorically found products- <br> '
                    for product in products2:
                        st = str(st) + " <br> " + str(
                            product.product_name) + " <br> " + "https:/" + "/personal-shopper-website.herokuapp.com/product/" + str(
                            product.id) + "/" + str(product.slug) + " <br> "
                    if products.count() > 0:
                        st = 'Products found- <br> '
                    for product in products:
                        st = str(st) + " <br> " + str(
                            product.product_name) + " <br> " + "https:/" + "/personal-shopper-website.herokuapp.com/product/" + str(
                            product.id) + "/" + str(product.slug) + " <br> "
                    print(st)
                    chat_response = st
                    print(chat_response)
                else:
                    chat_response = "No product available with these specifications."
            except:
                chat_response = chatbot.get_response(data).text
        elif data.find('product:') == 0:
            try:
                data = data[8:]
                products_i = Product.objects.filter(product_name__icontains=data)
                print(products_i.count())
                datalt = data.split(' ')
                print(datalt)
                x = len(datalt)
                print(x)
                prod = []
                for i in datalt:
                    products_k = Product.objects.filter(product_keywords__icontains=i)
                    prod.append(Product.objects.filter(product_keywords__icontains=i))
                    print(products_k.count())
                do = 0
                for i in prod:
                    if do == 0:
                        products = i
                    else:
                        products = products.intersection(i)
                    do = do + 1
                products = products_i.union(products)
                try:
                    catgoryids = Category.objects.values_list('id', flat=True).get(category_name__icontains=data)
                    products2 = Product.objects.filter(category_id=catgoryids)
                except:
                    products2 = Product.objects.none()
                print(products.count())
                if products.count() > 0 or products2.count() > 0:
                    st = ' '
                    if products2.count() > 0:
                        st = 'Categorically found products- <br> '
                    for product in products2:
                        st = str(st) + " <br> " + str(
                            product.product_name) + " <br> " + "https:/" + "/personal-shopper-website.herokuapp.com/product/" + str(
                            product.id) + "/" + str(product.slug) + " <br> "
                    if products.count() > 0:
                        st = 'Products found- <br> '
                    for product in products:
                        st = str(st) + " <br> " + str(
                            product.product_name) + " <br> " + "https:/" + "/personal-shopper-website.herokuapp.com/product/" + str(
                            product.id) + "/" + str(product.slug) + " <br> "
                    print(st)
                    chat_response = st
                    print(chat_response)
                else:
                    chat_response = "No product available with these specifications."
            except:
                chat_response = chatbot.get_response(data).text
        else:
            chat_response = chatbot.get_response(data).text

    else:
        chat_response = "No response"

    return HttpResponse(str(chat_response))


def home(request, template_name="home.html"):
    return render(request, template_name)
