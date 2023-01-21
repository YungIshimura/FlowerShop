import json
import uuid
from random import choice

from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from environs import Env
from more_itertools import chunked
from yookassa import Configuration, Payment

from .forms import OrderForm, RequestToConsultationForm
from .models import Bouquet, Bouquet_Flower, Occasion, Order, Shop


def processing_consultation_form(req):
    if req.method == 'POST':
        form = RequestToConsultationForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(
                req, 'Спасибо за обращение. Наши операторы перезвонят вам в близжайшее время'
            )
    else:
        form = RequestToConsultationForm()

    return form


def view_index(request):
    recommended_bouquets = Bouquet.objects.filter(is_recommended=True)
    context = {
        'recommended_bouquets': recommended_bouquets,
    }

    form = processing_consultation_form(request)
    context['form'] = form

    return render(request, 'Flower/index.html', context)


def view_catalog(request):
    bouquets = list(chunked(Bouquet.objects.all(), 3))
    context = {
        'recommended_bouquets': bouquets[0],
        'bouquets': bouquets[1:],
    }

    form = processing_consultation_form(request)
    context['form'] = form

    return render(request, 'Flower/catalog.html', context=context)


def view_quiz(request):
    context = {
        'occasions': Occasion.objects.all()
    }

    return render(request, 'Flower/quiz.html', context=context)


def view_quiz_step(request):
    request.session['occasion'] = request.GET.get('occasion')
    prices = set(
        f'{(bouquet.price // 1000) * 1000} - {(bouquet.price // 1000 + 1) * 1000} руб.'
        for bouquet in Occasion.objects.get(title=request.GET.get('occasion')).bouquets.all()
    )
    prices.add('Не имеет значения')
    context = {
        'intervals': sorted(prices)
    }

    return render(request, 'Flower/quiz-step.html', context=context)


def view_result(request):
    bouquets = Occasion.objects.get(
        title=request.session.get('occasion')).bouquets.all()

    if request.GET['price'] != 'Не имеет значения':
        min_price, max_price = ''.join(
            request.GET['price'].split(' руб.')).split(' - ')
        min_price, max_price = int(min_price), int(max_price)
        bouquets = [
            bouquet for bouquet
            in bouquets
            if min_price < bouquet.price < max_price
        ]
    shops = Shop.objects.all()
    context = {
        'bouquets': [
            {
                'id': bouquet.id,
                'title': bouquet.name,
                'description': bouquet.description,
                'image': bouquet.image.url,
                'price': bouquet.price,
                'flowers': bouquet.get_flowers()
            }
            for bouquet in bouquets
        ],
        'shops': shops
    }

    form = processing_consultation_form(request)
    context['form'] = form

    return render(request, 'Flower/result.html', context=context)


def view_card(request, bouquet_id):
    bouquet = Bouquet.objects.get(id=bouquet_id)
    bouquet_flowers = Bouquet_Flower.objects.filter(bouquet=bouquet)

    context = {
        'bouquet': bouquet,
        'bouquet_flowers': bouquet_flowers
    }

    form = processing_consultation_form(request)
    context['form'] = form

    response = render(request, 'Flower/card.html', context=context)
    response.set_cookie(key='bouquet_id', value=bouquet_id,
                        max_age=None, expires=None)

    return response


def view_order(request, bouquet_id):
    delivery_times = Order.TIME_OF_DELIVERY
    context = {
        'delivery_times': [delivery_time[1] for delivery_time in delivery_times]
    }
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            bouquet_id = bouquet_id or request.COOKIES.get('bouquet_id')
            bouquet = Bouquet.objects.get(id=bouquet_id)
            order = Order.objects.create(
                customer_name=request.POST['customer_name'],
                phonenumber=request.POST['phonenumber'],
                address=request.POST['address'],
                time=request.POST['time'],
                cost=bouquet.price,
                bouquet=bouquet
            )
            return HttpResponseRedirect(reverse('Flower:order-step', args=[order.id]))
    else:
        form = OrderForm()

    context['form'] = form

    return render(request, 'Flower/order.html', context=context)


def view_order_step(request, order_id):
    env = Env()
    env.read_env()

    yookassa_account_id = env('YOOKASSA_ACCOUNT_ID')
    yookassa_secret_key = env('YOOKASSA_SECRET_KEY')
    Configuration.account_id = yookassa_account_id
    Configuration.secret_key = yookassa_secret_key

    order = Order.objects.get(id=order_id)

    payment = Payment.create({
        "amount": {
            "value": f'{order.cost}',
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": 'http://127.0.0.1:8000/'
        },
        "capture": True,
        "description": "Заказ №1"
    }, uuid.uuid4())

    url = json.loads(payment.json())['confirmation']['confirmation_url']

    return redirect(url)
