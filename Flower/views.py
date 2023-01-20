from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RequestToConsultationForm, OrderForm
from django.contrib import messages
from .models import Bouquet, Bouquet_Flower, Order
from django.shortcuts import render, HttpResponseRedirect
from yookassa import Configuration, Payment
import uuid
import json
from environs import Env

def view_index(request):
    recommended_bouquets = Bouquet.objects.filter(is_recommended=True)
    context = {
        'recommended_bouquets': recommended_bouquets,
    }
    if request.method == 'POST':
        form = RequestToConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Спасибо за обращение. Наши операторы перезвонят вам в близжайшее время'
            )
            return redirect(request.path)
    else:
        form = RequestToConsultationForm()

    context['form'] = form

    return render(request, 'Flower/index.html', context)


def view_catalog(request):
    bouquets = Bouquet.objects.all()
    context = {
        'bouquets': bouquets[:3],
    }
    return render(request, 'Flower/catalog.html', context=context)


def view_quiz(request):

    return render(request, 'Flower/quiz.html')


def view_quiz_step(request):

    return render(request, 'Flower/quiz-step.html')


def view_result(request):

    return render(request, 'Flower/result.html')


def view_card(request, bouquet_id):
    bouquet = Bouquet.objects.get(id=bouquet_id)
    bouquet_flowers = Bouquet_Flower.objects.filter(bouquet=bouquet)
    context = {
        'bouquet': bouquet,
        'bouquet_flowers': bouquet_flowers
    }
    response = render(request, 'Flower/card.html', context=context)
    response.set_cookie(key='bouquet_id', value=bouquet_id, max_age=None, expires = None)

    return response


def view_order(request):
    delivery_times = Order.TIME_OF_DELIVERY
    context = {
        'delivery_times': [delivery_time[1] for delivery_time in delivery_times]
    }
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            bouquet_id = request.COOKIES.get('bouquet_id')
            bouquet = Bouquet.objects.get(id=bouquet_id)
            order=Order.objects.create(
                customer_name = request.POST['customer_name'],
                phonenumber = request.POST['phonenumber'],
                address = request.POST['address'],
                time = request.POST['time'],
                cost = bouquet.price,
                bouquet = bouquet                  
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