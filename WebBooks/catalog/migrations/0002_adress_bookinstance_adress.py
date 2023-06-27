# Generated by Django 4.2.2 on 2023-06-25 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите адрес магазина', max_length=100, verbose_name='Адрес магазина')),
            ],
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='adress',
            field=models.ForeignKey(default=1, help_text='Адрес магазина', on_delete=django.db.models.deletion.CASCADE, to='catalog.adress', verbose_name='Адрес магазина'),
            preserve_default=False,
        ),
    ]