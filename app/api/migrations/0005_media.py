# Generated by Django 4.1.5 on 2023-03-15 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_on_api', models.CharField(max_length=300)),
                ('image_on_api', models.TextField()),
                ('name_on_api', models.CharField(max_length=300)),
                ('register_date', models.DateField(auto_now_add=True)),
                ('goal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.goal')),
                ('mediatype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.mediatype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
