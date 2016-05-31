from urllib2 import URLError
from datetime import datetime
import requests
import stripe

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.mail import send_mail

from geopy.geocoders import GoogleV3, Nominatim
from geopy.exc import GeocoderQueryError

from .forms import *
from .models import *
from allauth.socialaccount.models import *

def get_sellers(location):
    '''
    get sellers cover the current location and  return then in distance order
    '''
    # get open and shortest delivery hour
    now = datetime.now()
    weekday = now.isoweekday()
    # filter workday and time
    sellers = Seller.objects.filter(operating_days__id=weekday, open_hour__lte=now.time(), close_hour__gte=now.time())
    sellers_id = [seller.id for seller in sellers]

    current_point = geos.fromstr("POINT(%s)" % location)
    dis_sellers = Seller.gis.distance(current_point)
    # sort by estimated delivery time    
    dis_sellers = dis_sellers.filter(id__in=sellers_id).order_by('estimated_delivery') 
    # filter only in radius
    sellers = [seller for seller in dis_sellers if seller.distance.mi <= seller.radius]
    return sellers

def get_client_ip(request):
    '''
    get ip from the request
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_location_with_ip(ip):
    FREEGEOPIP_URL = 'http://freegeoip.net/json'
    url = '{}/{}'.format(FREEGEOPIP_URL, ip)

    response = requests.get(url)
    response.raise_for_status()
    out = response.json()

    return out['latitude'], out['longitude']

def home(request):
    return render(request, 'landing.html')

def buy(request):    
    if request.POST:
        location2 = request.POST['address']
        sellers = get_sellers(location2)
        lnglat = location2.split(' ')
        location1 = '%s,%s' % (lnglat[1], lnglat[0])
        map_rendered = request.POST['map_rendered']
    else:
        ip = get_client_ip(request) 
        ip = '142.33.135.231' # this is the test location on dev
        lat, lon = get_client_location_with_ip(ip)
        location1 = '%f, %f' % (lat, lon)
        location2 = '%f %f' % (lon, lat)    # geopy location
        sellers = get_sellers(location2)
        map_rendered = None

    return render(request, 'buy.html', {
        'sellers': sellers, 
        'location1': location1, 
        'location2': location2,
        'map_rendered': map_rendered
    })

@csrf_exempt
def start_order(request):
    id = request.POST.get('id')
    location = request.POST.get('location')
    distance = request.POST.get('distance')
    geolocator = Nominatim()
    address = geolocator.reverse(location)

    seller = Seller.objects.get(id=id)
    initial_data = model_to_dict(seller)
    initial_data['address'] = address
    # initial_data['address'] = location
    initial_data['distance'] = distance+' miles away'

    form = OrderForm(initial=initial_data)

    return render(request, 'order.html', {
        'form': form, 
        'key': settings.STRIPE_KEYS['PUBLIC_KEY']
    })


def charge(request):
    form = OrderForm(request.POST)
    if form.is_valid():
        seller_email = form.cleaned_data['email']
        seller = Seller.objects.get(email=seller_email)
        price_in_cents = int(seller.unit_price * float(form.cleaned_data['quantity']))

        card = request.POST.get('stripeToken')
        stripe.api_key = settings.STRIPE_KEYS['API_KEY']
        stripe_account_id = SocialAccount.objects.get(user__id=seller.id, provider='stripe').uid

        charge = stripe.Charge.create(
            amount=price_in_cents,
            currency="usd",
            source=card,
            destination=stripe_account_id,
            application_fee = int(price_in_cents * 0.30),
            description='Thank you for your purchase!'            
        )

        sale = Sale()
        sale.seller = seller
        sale.quantity = float(form.cleaned_data['quantity'])
        sale.delivery_address = form.cleaned_data['address']
        sale.buyer_name = form.cleaned_data['buyer_name']
        sale.buyer_phone = form.cleaned_data['buyer_phone']
        sale.charge_id = charge.id
        sale.save()

        # send email
        email_subject = 'Order Confirmation'    
        email_body = "Dear %s.\n\nYou've got an order from Customer: %s \nAddress: %s\nPhone Number: %s\nQuantity: %.2f\nPlease confirm the order and fulfill it.\n\nThank you." % (seller.first_name, sale.buyer_name, sale.delivery_address, sale.buyer_phone, sale.quantity)
        send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [seller.email], fail_silently=False)

        return render(request, 'order_success.html', {'seller': seller})

    return render(request, 'order.html', {
        'form': form, 
        'key': settings.STRIPE_KEYS['PUBLIC_KEY']
    })

def login(request):
	return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')    

# login required for creating new seller account
@login_required(login_url='/login/')
def seller(request):
    seller = Seller.objects.get(username=request.user)

    if request.method == 'GET':
        form = SellerForm(initial=model_to_dict(seller))
    else:
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():         
            seller.first_name = form.cleaned_data['first_name']
            seller.open_hour = form.cleaned_data['open_hour']
            seller.close_hour = form.cleaned_data['close_hour']
            seller.address = form.cleaned_data['address']
            seller.phone = form.cleaned_data['phone']
            seller.radius = form.cleaned_data['radius']
            seller.item = form.cleaned_data['item']
            seller.unit_price = form.cleaned_data['unit_price']
            seller.picture = form.cleaned_data['picture']
            seller.description = form.cleaned_data['description']
            seller.min_order_amount = form.cleaned_data['min_order_amount']
            seller.permit_number = form.cleaned_data['permit_number']
            seller.permit_exp = form.cleaned_data['permit_exp']
            # seller.license = form.cleaned_data['license']
            seller.operating_days = form.cleaned_data['operating_days']
            seller.estimated_delivery = form.cleaned_data['estimated_delivery']
            seller.save()

            return HttpResponseRedirect('/login/')

    open_hour = seller.open_hour.hour * 60 + seller.open_hour.minute
    close_hour = seller.close_hour.hour * 60 + seller.close_hour.minute

    return render(request, 'seller.html', {'form': form, 'open_hour': open_hour, 'close_hour': close_hour })
