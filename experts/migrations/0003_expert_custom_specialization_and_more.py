# Generated by Django 5.1.6 on 2025-04-01 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experts', '0002_expert_specialization'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='custom_specialization',
            field=models.CharField(blank=True, max_length=255, verbose_name='Своя специализация'),
        ),
        migrations.AlterField(
            model_name='expert',
            name='specialization',
            field=models.CharField(blank=True, choices=[('developer', 'Разработчик'), ('designer', 'Дизайнер'), ('marketing', 'Маркетинг'), ('finance', 'Финансы'), ('other', 'Другое')], max_length=255, verbose_name='Специализация'),
        ),
    ]
