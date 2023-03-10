from django.urls import path

from .views import (view_card, view_catalog, view_index, view_order,
                    view_order_step, view_quiz, view_quiz_step, view_result)

app_name = 'Flower'

urlpatterns = [
    path('', view_index, name='index'),
    path('catalog', view_catalog, name='catalog'),
    path('order/<int:bouquet_id>/', view_order, name='order'),
    path('order-step/<int:order_id>/', view_order_step, name='order-step'),
    path('quiz', view_quiz, name='quiz'),
    path('quiz-step', view_quiz_step, name='quiz-step'),
    path('result', view_result, name='result'),
    path('card/<int:bouquet_id>/', view_card, name='card')
]
