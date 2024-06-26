# Generated by Django 4.2.9 on 2024-04-22 16:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_rename_communityactivity_communityactionstep_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemPartnerCommitment',
            fields=[
                ('commitment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('commitment_number', models.CharField(help_text='Automatically generated. No need to set manually.', max_length=10)),
                ('commitment_name', models.CharField(max_length=255)),
                ('commitment_details', models.TextField(max_length=1500)),
                ('commitment_lead', models.CharField(blank=True, default='', help_text='Indicate who will lead the commitment (person, organization, or team).', max_length=100)),
                ('commitment_status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Ongoing', 'Ongoing')], max_length=25)),
                ('completedby_year', models.CharField(choices=[('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('N/A', 'N/A')], max_length=4)),
                ('completedby_quarter', models.CharField(choices=[('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4'), ('N/A', 'N/A')], max_length=3)),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.goal')),
                ('related_objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.objective')),
                ('related_strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.strategy')),
                ('related_systempartner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.systempartner')),
            ],
            options={
                'verbose_name': 'System Partner Commitment',
                'verbose_name_plural': 'System Partner Commitments',
                'db_table': 'system_partner_commitments',
                'ordering': ['related_systempartner', 'related_goal', 'related_objective', 'related_strategy', 'commitment_number', 'completedby_year'],
            },
        ),
    ]
