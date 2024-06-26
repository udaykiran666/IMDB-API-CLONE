# Generated by Django 5.0.4 on 2024-05-29 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0008_reviews_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='total_reviews',
            field=models.IntegerField(default=0),
        ),
    ]
