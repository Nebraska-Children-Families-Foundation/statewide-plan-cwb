# Generated by Django 4.2.9 on 2024-02-26 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_strategyactivity_activity_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityactivity',
            name='activity_details',
            field=models.TextField(max_length=1200),
        ),
        migrations.AlterField(
            model_name='communityactivity',
            name='completedby_quarter',
            field=models.CharField(blank=True, choices=[('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4')], max_length=2),
        ),
        migrations.AlterField(
            model_name='communityactivity',
            name='completedby_year',
            field=models.CharField(blank=True, choices=[('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027')], max_length=4),
        ),
    ]
