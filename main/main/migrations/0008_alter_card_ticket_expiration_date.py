# Generated by Django 4.0 on 2022-01-08 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_card_id_alter_cardowner_id_alter_seller_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='ticket_expiration_date',
            field=models.DateField(null=True),
        ),
    ]
