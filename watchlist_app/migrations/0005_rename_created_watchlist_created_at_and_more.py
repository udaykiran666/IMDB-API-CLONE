# Generated by Django 5.0.4 on 2024-05-15 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0004_reviews'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]