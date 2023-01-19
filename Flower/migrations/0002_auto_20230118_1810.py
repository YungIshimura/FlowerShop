# Generated by Django 3.2.10 on 2023-01-18 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flower', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bouquet',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Изображение букета'),
        ),
        migrations.AlterField(
            model_name='bouquet',
            name='description',
            field=models.TextField(verbose_name='Описание букета'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('Raw', 'Не обработанный'), ('Processed', 'Обработанный')], default='Raw', max_length=50, verbose_name='Статус консультации'),
        ),
    ]