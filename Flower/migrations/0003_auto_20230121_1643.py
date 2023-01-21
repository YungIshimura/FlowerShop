# Generated by Django 3.2.10 on 2023-01-21 16:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Flower', '0002_auto_20230120_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decoration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.CharField(max_length=200, verbose_name='Описание')),
                ('color', models.CharField(blank=True, choices=[('white', 'белый'), ('black', 'черный'), ('yellow', 'желтый'), ('red', 'красный'), ('blue', 'синий'), ('green', 'зеленый'), ('orange', 'оранжевый'), ('sky_blue', 'небесный'), ('purple', 'фиолетовый')], max_length=100, verbose_name='Основной цвет')),
                ('price', models.SmallIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Изображение')),
            ],
        ),
        migrations.AlterField(
            model_name='bouquet_flower',
            name='flower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bouquet_flower', to='Flower.flower', verbose_name='Цветок в букете'),
        ),
        migrations.AlterField(
            model_name='order',
            name='bouquet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='Flower.bouquet', verbose_name='Букет'),
        ),
        migrations.CreateModel(
            name='BouquetDecoration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество')),
                ('bouquet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bouquet_decorations', to='Flower.bouquet', verbose_name='Букет')),
                ('decoration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bouquet_decorations', to='Flower.decoration', verbose_name='Декорация')),
            ],
        ),
    ]