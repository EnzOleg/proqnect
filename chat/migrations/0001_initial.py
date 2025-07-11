# Generated by Django 5.1.4 on 2025-02-08 15:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_type', models.CharField(choices=[('consultation', 'Консультанция'), ('social', 'Социальный')], default='social', max_length=20, verbose_name='Тип чата')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('booking', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='booking.booking', verbose_name='Бронирование')),
                ('participants', models.ManyToManyField(related_name='chats', related_query_name='Участники', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Сообщение')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')),
                ('read', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chat', verbose_name='Чат')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
        ),
    ]
