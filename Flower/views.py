from django.shortcuts import render


def view_index(request):

    return render(request, 'Flower/index.html')


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