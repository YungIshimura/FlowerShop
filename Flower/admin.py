from django.contrib import admin
from .models import Shop, Flower, Bouquet_Flower, Bouquet, Request, Order


class BouquetFlowerInline(admin.TabularInline):
    model = Bouquet_Flower


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    pass


@admin.register(Bouquet_Flower)
class BouquetFlowerAdmin(admin.ModelAdmin):
    pass


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    inlines = [
        BouquetFlowerInline
    ]


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
