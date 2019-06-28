# -*- coding: utf-8 -*-

from django.shortcuts import render

from dashboard.models import Orders, LegalEntities, Bids, Runs
import datetime
import requests
import json
from django.db.models import Max, Min, Count
from operator import itemgetter


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
    manager = 'Unknown'
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

    if order.customer_legal_entity.id in [3021, 3072, 2980]:
        manager = 'Voytik'
    if order.customer_legal_entity in [309]:
        manager = 'Trubicin'
    if order.customer_legal_entity in [579, 2798]:
        manager = 'Sudakov'
    if order.customer_legal_entity in [759]:
        manager = 'Ivaeva'

    if order.customer_legal_entity.id == 117:
        manager = 'Voytik'



    return [order.id,
            order.customer_legal_entity.organization_name,
            order.sender_locality_name,
            order.recipient_locality_name,
            order.price,
            float(order.price) * 0.9,
            float(order.price) * 0.9 * 0.8,
            status,
            manager
            ]


# Create your views here.
def index(request):
    objects = Orders.objects.filter(cargo_kind__in=['metal', 'other'], created_at__gte=datetime.date(2019, 6, 17),
                                    status__in=[4, 6, 9])
    orders_output = []
    for object in objects:
        orders_output.append(get_order_output_details(object))

    return render(request, 'dashboard/index.html', {'orders': orders_output})


def carriers(request, order_id):
    order = Orders.objects.get(id=order_id)
    similar_orders = Orders.objects.filter(sender_name=order.sender_name, recipient_name=order.recipient_name,
                                           created_at__gte=datetime.date(2019, 1, 1))

    runs = Runs.objects.filter(order__in=similar_orders)


    bids = Bids.objects.filter(order__in=similar_orders)

    bids_by_carrier = bids.values('executor_legal_entity_id').annotate(min_price=Min('price'), max_price=Max('price'))

    carriers_output = []

    for bid_by_carrier in bids_by_carrier:
        min_bid = bids.filter(price=bid_by_carrier['min_price'],
                              executor_legal_entity=bid_by_carrier['executor_legal_entity_id']).order_by('price').first()
        carrier = LegalEntities.objects.get(id=bid_by_carrier['executor_legal_entity_id'])

        count = runs.filter(executor_legal_entity=bid_by_carrier['executor_legal_entity_id']).count()



        carriers_output.append([carrier,
                                count,
                                bid_by_carrier['min_price'],
                                min_bid.order.id,
                                min_bid.created_at,
                                min_bid.vat_rate
                                ])


    return render(request, 'dashboard/carriers.html', {'carriers': sorted(carriers_output, key=itemgetter(1), reverse=True),
                                                       'order': get_order_output_details(order)})
