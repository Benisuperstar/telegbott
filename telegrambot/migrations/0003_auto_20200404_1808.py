# Generated by Django 3.0.5 on 2020-04-04 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegrambot', '0002_auto_20200404_0012'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bonus',
            options={'verbose_name': ('Бонус',), 'verbose_name_plural': 'Бонусы'},
        ),
        migrations.AlterField(
            model_name='bonus',
            name='bonus',
            field=models.PositiveIntegerField(verbose_name='Бонус'),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='telegrambot.Profile', verbose_name='Профиль'),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure', models.TextField(verbose_name='Место посадки')),
                ('place_of_arrival', models.TextField(verbose_name='Место прибытия')),
                ('time_departure', models.DateTimeField(verbose_name='Время посадки')),
                ('time_place_of_arrival', models.DateTimeField(verbose_name='Время прибытия')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='telegrambot.Profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': ('Поездка',),
                'verbose_name_plural': 'Поездки',
            },
        ),
    ]