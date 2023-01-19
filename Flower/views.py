from django.shortcuts import render, redirect
from .forms import RequestToConsultation
from django.contrib import messages


def view_index(request):
    context = {}
    if request.method == 'POST':
        form = RequestToConsultation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Спасибо за обращение. Наши операторы перезвонят вам в близжайшее время'
            )
            return redirect(request.path)
    else:
        form = RequestToConsultation()

    context['form'] = form

    return render(request, 'Flower/index.html', context)


def view_catalog(request):

    return render(request, 'Flower/catalog.html')


def view_order(request):

    return render(request, 'Flower/order.html')


def view_order_step(request):

    return render(request, 'Flower/order-step.html')


def view_quiz(request):

    return render(request, 'Flower/quiz.html')


def view_quiz_step(request):

    return render(request, 'Flower/quiz-step.html')


def view_result(request):

    return render(request, 'Flower/result.html')
