# -*- coding: utf-8 -*-

from django.shortcuts import render

from dashboard.models import Orders, LegalEntities, Bids, Runs, Users
import datetime
import requests
import json
from django.db.models import Max, Min, Count
from operator import itemgetter
from datetime import date



def get_yandex_address_obj(input_address):
    url = 'https://geocode-maps.yandex.ru/1.x/?apikey=5fddde38-1c3f-46b9-9a54-ae30942798e3&format=json&geocode='

    response = requests.get(url + input_address)
    result = json.loads(response.content)

    response_object = result['response']['GeoObjectCollection']['featureMember'][0]
    address_obj = response_object['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']

    # formatted
    formatted = address_obj['formatted']

    # city
    city = ''
    region = ''
    country = ''
    street = ''
    components = address_obj['Components']
    for component in components:
        if component['kind'] == 'country':
            country = component['name']
        if component['kind'] == 'locality':
            city = component['name']
        if component['kind'] == 'province':
            region = component['name']
        if component['kind'] == 'street':
            street = component['name']

    return [formatted, country, region, city, street,
            [float(response_object['GeoObject']['Point']['pos'].split(' ')[0]),
             float(response_object['GeoObject']['Point']['pos'].split(' ')[1])]]


def get_order_output_details(order):

    status = map_status(order)
    manager = get_manager(order)

    order_late = (datetime.datetime.now().date()-order.date_from.date()).days
    if order.sender_locality_name:
        sender_city = order.sender_locality_name
    else:
        sender_city = order.sender_dependent_locality_name

    if order.recipient_locality_name:
        recipient_city = order.recipient_locality_name
    else:
        recipient_city = order.recipient_dependent_locality_name

    if order.distance != 0:
        rate_without_nds = float(order.price) * 0.9 / 1.2 / order.distance
        rate_with_nds = float(order.price) * 0.9 / order.distance
    else:
        rate_without_nds = -1
        rate_with_nds = -1


    return [order.id,
            order.customer_legal_entity.organization_name,
            sender_city,
            recipient_city,
            order.price,
            float(order.price) * 0.9,
            float(order.price) * 0.9 / 1.2,
            status,
            manager,
            order.date_from,
            order_late,
            rate_without_nds,
            rate_with_nds
            ]


# Create your views here.
def index(request):
    objects = Orders.objects.filter(cargo_kind__in=['metal', 'other'], created_at__gte=datetime.date(2019, 6, 17),
                                    status__in=[4, 6])
    orders_output = []
    for object in objects:
        orders_output.append(get_order_output_details(object))

    return render(request, 'dashboard/index.html', {'orders': orders_output})


def carriers(request, order_id):
    order = Orders.objects.get(id=order_id)
    similar_orders = Orders.objects.filter(sender_region_id=order.sender_region_id,
                                           created_at__gte=datetime.date(2019, 1, 1),
                                           cargo_kind__in = ['metal', 'other'])

    runs = Runs.objects.filter(order__in=similar_orders)

    bids = Bids.objects.filter(order__in=similar_orders)

    bids_by_carrier = bids.values('executor_legal_entity_id').annotate(min_price=Min('price'), max_price=Max('price'))

    carriers_output = []

    for bid_by_carrier in bids_by_carrier:
        min_bid = bids.filter(price=bid_by_carrier['min_price'],
                              executor_legal_entity=bid_by_carrier['executor_legal_entity_id']).order_by('price').first()
        carrier = LegalEntities.objects.get(id=bid_by_carrier['executor_legal_entity_id'])

        count = runs.filter(executor_legal_entity=bid_by_carrier['executor_legal_entity_id']).count()

        admin = Users.objects.filter(company_id=carrier.company_id, roles__icontains='company_admin').first()

        carriers_output.append([carrier,
                                count,
                                bid_by_carrier['min_price'],
                                min_bid.order.id,
                                min_bid.created_at,
                                min_bid.vat_rate,
                                admin
                                ])


    return render(request, 'dashboard/carriers.html', {'carriers': sorted(carriers_output, key=itemgetter(1), reverse=True),
                                                       'order': get_order_output_details(order)})


def get_manager(order):
    manager = 'Unknown'

    if order.customer_legal_entity.id in [3021, 3072, 2980, 470]:
        manager = 'Войтик'
    elif order.customer_legal_entity.id in [579, 2798]:
        manager = 'Судаков'

    elif order.customer_legal_entity.id in [759]:
        manager = 'Иваева'

    elif order.customer_legal_entity.id in [309]:
        manager = 'Трубицин'


    elif order.sender_region_id in [19,17,32,20,41,35,49,75,81,74,76,50,43,77,78,33,55,51,71,66,67,24]:
        manager = 'Говоров'
    elif order.sender_region_id in [60,73,48,36,28,30,23,38,14,25,3,45,1,11,72,45]:
        manager = 'Борзова'
    elif order.sender_region_id in [37, 56, 29, 70, 59, 44, 34, 64, 65, 79, 46, 69, 62, 52, 54, 39, 63]:
        manager = 'Войтик'
    elif order.sender_region_id in [4, 27, 80, 15, 58, 16, 68, 42, 47, 21, 31, 8]:
        manager = 'Судаков'
    elif order.sender_region_id in [12, 5, 2, 18, 13, 9, 57, 26, 53]:
        manager = 'Иваева'
    elif order.sender_region_id in [166]:
        manager = 'Трубицин'




    return manager

def map_status(order):
    status = 'Unknown'
    if order.status == 4:
        # status = u'Ожидание исполнителя'
        status = order.status
    elif order.status == 9:
        # status = u'Не состоялся'
        status = order.status

    elif order.status == 6:
        if not Bids.objects.filter(order=order.id):
            # status = u'Новый'
            status = 60
        else:
            # status =  u'Подбор'
            status = 61
    return status
