# Generated by Django 5.1.6 on 2025-04-07 17:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_customuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_reg_number', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('company_website', models.URLField(blank=True, null=True)),
                ('business_address', models.TextField()),
                ('company_certificate', models.FileField(upload_to='documents/company_certificates/')),
                ('owner_id', models.FileField(upload_to='documents/owner_ids/')),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='images/company_logos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
