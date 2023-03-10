from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Shop(models.Model):
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес магазина'
    )
    phonenumber = PhoneNumberField(
        verbose_name='Номер телефона',
        db_index=True
    )

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class Flower(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название цветка'
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Цена',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цветок'
        verbose_name_plural = 'Цветы'


class Decoration(models.Model):
    COLORS = (
        ('white', 'белый'),
        ('black', 'черный'),
        ('yellow', 'желтый'),
        ('red', 'красный'),
        ('blue', 'синий'),
        ('green', 'зеленый'),
        ('orange', 'оранжевый'),
        ('sky_blue', 'небесный'),
        ('purple', 'фиолетовый'),
    )
    title = models.CharField('Название', max_length=100)
    description = models.CharField('Описание', max_length=200)
    color = models.CharField('Основной цвет', max_length=100, choices=COLORS, blank=True)
    price = models.SmallIntegerField(
        'Стоимость',
        validators=[MinValueValidator(0)],
        blank=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True
    )

class BouquetDecoration(models.Model):
    decoration = models.ForeignKey(
        'Decoration',
        related_name='bouquet_decorations',
        on_delete=models.CASCADE,
        verbose_name='Декорация',
    )
    bouquet = models.ForeignKey(
        'Bouquet',
        related_name='bouquet_decorations',
        on_delete=models.CASCADE,
        verbose_name='Букет',
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество'
    )


class Bouquet(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название букета'
    )
    image = models.ImageField(
        verbose_name='Изображение букета'
    )
    description = models.TextField(
        verbose_name='Описание букета'
    )
    
    occasions = models.ManyToManyField(
        'Occasion',
        verbose_name='Для каких поводов',
        related_name='bouquets'
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='Цена',
    )
    is_recommended = models.BooleanField(
        default=False,
        verbose_name='Рекомендован'
    )
    height = models.CharField(
        max_length=120,
        verbose_name='Высота букета'
    )
    width = models.CharField(
        max_length=100,
        verbose_name='Ширина букета'
    )

    def __str__(self):
        return self.name

    def get_flowers(self):
        return [
            {
                'title': item.flower.name,
                'quantity': item.quantity
            }
            for item in self.bouquet_flower.all()
        ]

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Bouquet_Flower(models.Model):
    flower = models.ForeignKey(
        Flower,
        related_name='bouquet_flower',
        on_delete=models.PROTECT,
        verbose_name='Цветок в букете',
    )
    bouquet = models.ForeignKey(
        Bouquet,
        related_name='bouquet_flower',
        on_delete=models.CASCADE,
        verbose_name='Название букета',
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.flower} в {self.bouquet}'

    class Meta:
        verbose_name = 'Цветок в букете'
        verbose_name_plural = 'Цветы в букете'


class Order(models.Model):
    TIME_OF_DELIVERY = [
        ('FAST_AS_POSSIBLE', 'Как можно скорее'),
        ('FROM_10_TO_12', 'С 10:00 до 12:00'),
        ('FROM_12_TO_14', 'С 12:00 до 14:00'),
        ('FROM_14_TO_16', 'С 14:00 до 16:00'),
        ('FROM_16_TO_18', 'С 16:00 до 18:00'),
        ('FROM_18_TO_20', 'С 18:00 до 20:00')
    ]

    bouquet = models.ForeignKey(
        Bouquet,
        related_name='order',
        on_delete=models.PROTECT,
        verbose_name='Букет',
    )
    time = models.CharField(
        max_length=30,
        choices=TIME_OF_DELIVERY,
        verbose_name='Дата заказа'
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата заказа'
    )
    customer_name = models.CharField(
        max_length=255,
        verbose_name='Имя клиента',
    )
    cost = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Стоимость'
    )
    phonenumber = PhoneNumberField(
        verbose_name='Номер телефона'
    )
    address = models.CharField(
        max_length=100,
        verbose_name='Адрес доставки',
    )

    def __str__(self):
        return f'{self.bouquet} -- {self.phonenumber}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Request(models.Model):
    STATUS = [
        ('Raw', 'Не обработанный'),
        ('Processed', 'Обработанный')
    ]

    SOURCE = [
        ('Site', 'Сайт'),
        ('WA', 'WhatsApp'),
        ('TG', 'Telegram'),
        ('Phonecall', 'Звонок'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name='Имя клиента'
    )
    phonenumber = PhoneNumberField(
        db_index=True,
        verbose_name='Номер телефона'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS,
        default='Raw',
        verbose_name='Статус консультации',
    )
    source = models.CharField(
        max_length=30,
        choices=SOURCE,
        default='Site',
        verbose_name='Откуда пришла заявка'
    )

class Occasion(models.Model):
    title = models.CharField('Повод', max_length=50)

    def __str__(self):
        return self.title
