# Generated by Django 4.0.2 on 2022-03-07 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=89, unique=True, verbose_name='category')),
            ],
            options={
                'verbose_name_plural': 'Products Categories',
            },
        ),
    ]
