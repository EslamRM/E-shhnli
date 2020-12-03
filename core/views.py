import requests
import random
from bs4 import BeautifulSoup
from ebaysdk.finding import Connection as finding
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render ,HttpResponse,redirect,Http404,get_object_or_404
from django.core.mail import send_mail
from project.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Order,Profile,CommercialOrder,Calculator,Subscribtion
from django.utils import translation
from .paymob import api_key,auth,transaction_res,pay,create_order
from django.views.generic.base import View
from django.views.generic import UpdateView

class ActivateLanguageView(View):
    language_code = ''
    redirect_to   = ''
    def get(self, request, *args, **kwargs):
        self.redirect_to = request.META.get('HTTP_REFERER')
        self.language_code = kwargs.get('language_code')
        translation.activate(self.language_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = self.language_code
        return redirect(self.redirect_to)


@login_required
def payments(request):
    profile = Profile.objects.filter(user=request.user)
    if profile:
        
        billing_info = {}
        for p in profile:
            billing_info = {"apartment":p.address_1,"email": p.user.email,"floor": "NA",
                            "first_name": p.full_name.split(' ')[0],
                            "street":p.address_2,"building":"NA",
                            "phone_number": str(p.phone_number),
                            "shipping_method": "PKG", "postal_code": p.ZIP,"city": p.address_1,
                            "country": p.country, "last_name": p.full_name.split(' ')[1],"state": p.state}
        step1 = auth(api_key)
        step2 = create_order(step1, request.POST.get('pay'), 'EGP')
        step3 = pay(step2,75358, billing_info)
        step4 = transaction_res(step3)
        iframe = "https://accept.paymob.com/api/acceptance/iframes/96321?payment_token="
        return HttpResponseRedirect(iframe + step3['payment_key'])
    
    else:
        return redirect('/accounts/register')
        
def index(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)
        return render(request, 'index.html', {'profile': profile})
    else:
        return render(request, 'index.html')

def how_work (request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)
        return render(request, 'how-work.html', {'profile': profile})
    else:
        return render(request, 'how-work.html')
def offers (request):
    if request.user.is_authenticated:
        proxies_list = ["128we199d10d9d24d1d80d80", "1e1y3fgje5yd3gj2edy39fgj3d18", "125v1b4n1v2b0n0v5b3nv8b0n",
                        "1a2z5m1a4z1m2a0z0ma1z4m80",
                        "128d19d9d20d0d11d2d13d8", "1e4y9fgje5yd6gj1edy2d9gj3d18", "128v1b9n9v2b0n0v1b1n2v8b0n",
                        "1a2z5m1a4z1m2a0z0ma3z9m80",
                        "134d21d3d29dd20d2d44d44"]
        coupon = random.choice(proxies_list)
        profile = Profile.objects.filter(user=request.user)
        return render(request,'offer.html',{'coupon':coupon,'profile':profile})
    else:
        proxies_list = ["128we199d10d9d24d1d80d80", "1e1y3fgje5yd3gj2edy39fgj3d18", "125v1b4n1v2b0n0v5b3nv8b0n",
                        "1a2z5m1a4z1m2a0z0ma1z4m80",
                        "128d19d9d20d0d11d2d13d8", "1e4y9fgje5yd6gj1edy2d9gj3d18", "128v1b9n9v2b0n0v1b1n2v8b0n",
                        "1a2z5m1a4z1m2a0z0ma3z9m80",
                        "134d21d3d29dd20d2d44d44"]
        coupon = random.choice(proxies_list)
        return render(request,'offer.html',{'coupon':coupon})

@login_required
def orders(request):
    profile = Profile.objects.filter(user=request.user)
    commercial = CommercialOrder.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    items = orders.count() + commercial.count()
    return render(request,'com.html',{'orders':orders,'items':items,'profile':profile,'commercial':commercial})
@login_required
def order(request):
    profile = Profile.objects.filter(user=request.user)
    calculate = Calculator.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request,'order.html',{'orders':orders,'profile':profile,'calculate':calculate})
def support (request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        send_mail(subject=name, message=message, from_email=request.user, recipient_list=[EMAIL_HOST_USER],
                  fail_silently=False)
        return HttpResponse('Email has been send successfully')

    elif request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)
        return render(request,'support.html',{'profile':profile})

    else:
        return render(request,'support.html')



def faq (request):
    profile = Profile.objects.filter(user=request.user)
    return render(request,'faq.html',{'profile':profile})


@login_required
def com(request):
    if request.method == 'POST':
        price = request.POST['com_price']
        price = ','.join([price[i:i+3] for i in range(0,len(price),3)])
        commercial = CommercialOrder(
            title=request.POST['com_title'],
            quantity=request.POST['com_quantity'],
            price=price +' EGP',
            details=request.POST['com_text'],
            file=request.FILES.get('com_file'),
        )
        commercial.user=request.user
        commercial.save()
        return HttpResponseRedirect('/orders/com/')
    else:
        profile = Profile.objects.filter(user=request.user)
        commercial = CommercialOrder.objects.filter(user=request.user)
        calculate = Calculator.objects.filter(user=request.user)
        orders = Order.objects.filter(user=request.user)
        items = orders.count() + commercial.count()
        return render(request,'com.html',{'orders':orders,'items':items,'profile':profile,'calculate':calculate,'commercial':commercial})

@login_required
def com_all(request):
    commercial = CommercialOrder.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    items = orders.count() + commercial.count()
    return render(request, 'com.html', {'commercial': commercial, 'orders': orders, 'items': items})

@login_required
def cart(request):
    if request.user.is_authenticated:
        calculate = Calculator.objects.filter(user=request.user)
        orders = Order.objects.filter(user=request.user)
        profile = Profile.objects.filter(user=request.user)
        count = orders.count()
    else:
        return redirect('/accounts/login/')
    return render(request, 'cart.html',{'orders':orders,'count':count,'calculate':calculate,'profile':profile})

def clear_com(request):
    clear_com = CommercialOrder.objects.filter(user=request.user)
    clear_com.delete()
    return HttpResponseRedirect('/orders/com')
def clear_item_com(request,id):
    order_com = get_object_or_404(CommercialOrder,id=id)
    order_com.delete()
    return HttpResponseRedirect('/orders/com')
def edit_item_com(request,id):
    order_com = get_object_or_404(CommercialOrder, id=id)
    order_com.title = request.POST.get('title1')
    order_com.quantity = request.POST.get('qty1')
    order_com.price = request.POST.get('price1')
    order_com.details = request.POST.get('details1')
    order_com.save()
    return HttpResponseRedirect('/orders/com')
def clear_cart(request):
    clear_orders=Order.objects.filter(user=request.user)
    clear_orders.delete()
    return HttpResponseRedirect('/cart')

def clear_item(request,id):
    item = get_object_or_404(Order,id=id)
    item.delete()
    return HttpResponseRedirect('/cart')
def edit_item(request,id):
    if request.method == 'POST':
        edit = get_object_or_404(Order,id=id)
        edit.title = request.POST.get('title')
        edit.category = request.POST.get('category')
        edit.size = request.POST.get('size')
        edit.color = request.POST.get('color')
        edit.Qty = request.POST.get('qty')
        edit.save()
        return HttpResponseRedirect('/cart')
    else:
        return HttpResponseRedirect('/cart')
@login_required
def add_cart(request):
    if request.method == 'POST':
        new = Order(logo_url=request.POST['logo'],
                    title=request.POST['title'],
                    price=request.POST['price'],
                    img_url=request.POST['img'],
                    url=request.POST['url'],
                    category=request.POST['category'],
                    color=request.POST['color'],
                    size=request.POST['size'],
                    Qty=request.POST['qty'],
                    promo=request.POST['promo'],
                    )
        new.user = request.user
        new.save()
        return HttpResponseRedirect('/cart')
    else:
        return redirect('/')

@login_required
def update(request,username):
    if request.method == 'POST':
        new = get_object_or_404(User,username=username)
        user = new.profile
        user.full_name = request.POST.get('full_name')
        new.email = request.POST.get('email')
        new.save()
        user.address_1 = request.POST.get('address_1')
        user.address_2 = request.POST.get('address_2')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        return HttpResponseRedirect(request.path_info)
    else:
        profile = Profile.objects.filter(user=request.user)
    return render(request,'base.html',{'profile':profile})
@login_required
def subscribe(request):
    if request.method == 'POST':
        sub = Subscribtion(subscribe=request.POST.get('subscribe'))
        sub.user = request.user
        sub.save()
        return HttpResponseRedirect(request.path_info)
    else:
        return redirect('/')

#- ecommerce sites api

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
proxies = {'https': random.choice(proxies_list)}

# for ebay
# URL = 'https://www.ebay.com/p/9034209182?iid=114157441243'
#
# page = requests.get(URL,headers=headers)
# soup = BeautifulSoup(page.content,features='lxml')
# soup.findAll(True,{'class':'product-title','id':'itemTitle'})
# # title = soup.find(id='itemTitle').text
# # price = soup.find(id='prcIsum').text
# # #img = soup.find_all(class_='img')[0].find_all('img')[-1]['src']
# # img = soup.find_all(class_='vi-image-gallery__image vi-image-gallery__image--absolute-center')
# selectors = ['.product-title', '#itemTitle']
# inf = []
# for s in selectors:
#     inf.append(soup.find_all(attrs=s))
#
# print(inf)
# print(img)

# ID_APP = 'EslamRam-shahnli-PRD-6c8eaa52b-95f85fe5'
#
# Keywords =
# api = finding(appid=ID_APP, config_file=None)
# api_request = { 'keywords': Keywords }
# response = api.execute('findItemsByKeywords', api_request)
# soup = BeautifulSoup(response.content,'lxml')
#
# totalentries = int(soup.find('totalentries').text)
# items = soup.find_all('item')
#
# for item in items:
#     cat = item.categoryname.string.lower()
#     title = item.title.string.lower()
#     price = int(round(float(item.currentprice.string)))
#     url = item.viewitemurl.string.lower()
# #########################
import re
def api(request):
    if request.method == 'POST':
        URL = request.POST['url']
        if not re.match('(?:http|ftp|https)://', URL):
            print(URL)
            raise Http404("Enter A Valid URL")

        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, features='lxml')

        if '6pm.com' in URL:
            try:
                logo = URL.split('/')[2]
                title = soup.find(class_='av').text
                price = soup.find(class_='dr ir').text
                img = soup.find(class_='lt')['src']
                context = {
                    'title':title,
                    'price':price,
                    'img':img,
                    'url':URL,
                    'logo':logo,
                }
                return render(request,'cart.html',context)
            except:
                return render(request,'cart.html')
        elif 'carters.com' in URL:
            try:
                logo = URL.split('/')[2]
                title = soup.find(class_='product-title').text.strip()
                price = soup.find(class_='value').text.strip()
                img = soup.find(class_='js-product-main-image-0')['data-yo-src']
                context = {
                    'title': title,
                    'price': price,
                    'img': img,
                    'url': URL,
                    'logo':logo,
                }
                return render(request, 'cart.html', context)
            except:
                return render(request,'cart.html')
        elif 'gap.com' in URL:
            try:
                logo = URL.split('/')[2]
                title = soup.find(class_="product-title__text").get_text(strip=True)
                price = soup.find(class_="pdp-pricing__selected").text
                img = soup.find(class_="hover-zoom")['href']
                context = {
                    'title': title,
                    'price': price,
                    'img': 'https://www.gap.com'+img,
                    'url': URL,
                    'logo':logo,
                }
                return render(request, 'cart.html', context)
            except:
                return render(request,'cart.html')
        elif 'guess.eu' in URL:
            try:
                logo = URL.split('/')[2]
                title = soup.find(class_="pull-left").text
                price = soup.find(class_="actual").text
                img = soup.find_all(class_="zoom-link")[-1].find('img')
                img = img['src'][:84]+img['data-image']
                context = {
                    'title': title,
                    'price': price,
                    'img': img,
                    'logo':logo,
                    'url': URL,
                }
                return render(request, 'cart.html', context)
            except:
                return render(request,'cart.html')
        elif 'uspoloassn.com' in URL:
            try:
                logo = URL.split('/')[2]
                title = soup.find(class_="emos_H1").text
                price = soup.find(class_="urunDetay_satisFiyat").text
                img = soup.find_all(class_="mask")[-1].find_all('a')
                img = 'https://eg.uspoloassn.com/'+img[0]['href']
                context = {
                    'title': title,
                    'price': price,
                    'img': img,
                    'logo':logo,
                    'url': URL,
                }
                return render(request, 'cart.html', context)
            except:
                return render(request,'cart.html')
        elif 'ralphlauren.com' in URL:
            try:
                logo = URL.split('/')[2]
                title = soup.find(class_="product-name").text.strip()
                price = soup.find(class_="lowblack").text.strip()
                img = soup.find(class_="popup-img")['data-img']
                context = {
                    'title': title,
                    'price': price,
                    'img': img,
                    'url': URL,
                    'logo':logo,
                }
                return render(request, 'cart.html', context)
            except:
                return render(request, 'cart.html')
        else:
            return render(request,'cart.html')

