from django.db import models
from django.core.validators import MinValueValidator


class Flower(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='название цветка'
    )
    price = models.IntegerField(
        verbose_name='цена',
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='название букета'
    )
    description = models.TextField()

    def __str__(self):
        return self.name


class Bouquet_Flower(models.Model):
    flower = models.ForeignKey(
        Flower,
        verbose_name='цветок в букете',
        related_name='bouquet_flower',
        on_delete=models.CASCADE
    )
    bouquet = models.ForeignKey(
        Bouquet,
        verbose_name='название букета',
        related_name='bouquet_flower',
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='количество'
    )

    def __str__(self):
        return f'{self.flower} в {self.bouquet}'


class Order(models.Model):
    bouquet = models.ForeignKey(
        Bouquet,
        verbose_name='букет',
        related_name='order',
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата заказа'
    )
    customer_name = models.CharField(
        verbose_name='Имя клиента',
        max_length=255
    )
    number = models.CharField(
        verbose_name='номер клиента',
        max_length=11
    )
    address = models.CharField(
        verbose_name='адрес',
        max_length=255
    )
    cost = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='стоимость'
    )

    def __str__(self):
        return f'{self.bouquet} -- {self.address}'


class Request(models.Model):
    name = models.CharField(
        verbose_name='имя клиента',
        max_length=255
    )
    number = models.CharField(
        verbose_name='номер клиента',
        max_length=11
    )
    reason = models.CharField(
        verbose_name='причина',
        max_length=255
    )