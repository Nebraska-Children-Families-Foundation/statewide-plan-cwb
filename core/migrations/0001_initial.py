# Generated by Django 4.2.9 on 2024-02-05 16:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityStatus',
            fields=[
                ('activity_status_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('activity_status', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityCollaborative',
            fields=[
                ('community_collab_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('community_collab_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('goal_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('goal_number', models.IntegerField()),
                ('goal_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='NcffTeam',
            fields=[
                ('ncff_team_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ncff_team_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('objective_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('objective_number', models.IntegerField()),
                ('objective_name', models.CharField(max_length=255)),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.goal')),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('strategy_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('strategy_number', models.CharField(max_length=9)),
                ('strategy_name', models.CharField(max_length=255)),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.goal')),
                ('related_objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.objective')),
            ],
        ),
        migrations.CreateModel(
            name='StrategyActivity',
            fields=[
                ('activity_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('activity_number', models.CharField(max_length=10)),
                ('activity_name', models.CharField(max_length=255)),
                ('activity_details', models.TextField(max_length=500)),
                ('activity_lead', models.CharField(max_length=100)),
                ('activity_priority', models.BooleanField()),
                ('activity_status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Ongoing', 'Ongoing')], max_length=25)),
                ('completedby_year', models.CharField(choices=[('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027')], max_length=4)),
                ('completedby_quarter', models.CharField(choices=[('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4')], max_length=2)),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.goal')),
                ('related_objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.objective')),
                ('related_strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.strategy')),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceMeasure',
            fields=[
                ('measure_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('measure', models.CharField(max_length=255)),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.goal')),
            ],
        ),
        migrations.CreateModel(
            name='DhhsPriority',
            fields=[
                ('dhhs_priority_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('priority_description', models.CharField(max_length=255)),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.goal')),
            ],
        ),
        migrations.CreateModel(
            name='CommunityActivity',
            fields=[
                ('activity_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('activity_number', models.CharField(max_length=10)),
                ('activity_name', models.CharField(max_length=255)),
                ('activity_details', models.TextField(max_length=500)),
                ('activity_lead', models.CharField(max_length=100)),
                ('activity_status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Ongoing', 'Ongoing')], max_length=25)),
                ('completedby_year', models.CharField(choices=[('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027')], max_length=4)),
                ('completedby_quarter', models.CharField(choices=[('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4')], max_length=2)),
                ('related_collaborative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.communitycollaborative')),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.goal')),
                ('related_objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.objective')),
                ('related_strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.strategy')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeIndicator',
            fields=[
                ('indicator_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('indicator', models.CharField(max_length=255)),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.goal')),
            ],
        ),
        migrations.CreateModel(
            name='StrategyPriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_collab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.communitycollaborative')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.strategy')),
            ],
            options={
                'unique_together': {('strategy', 'community_collab')},
            },
        ),
    ]
