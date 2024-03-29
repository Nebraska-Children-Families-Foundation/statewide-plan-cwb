# Generated by Django 4.2.9 on 2024-02-21 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_strategy_related_objective'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitystatus',
            options={'ordering': ('activity_status',), 'verbose_name': 'Activity Status', 'verbose_name_plural': 'Activity Statuses'},
        ),
        migrations.AlterModelOptions(
            name='changeindicator',
            options={'ordering': ('indicator',), 'verbose_name': 'Indicator of Change', 'verbose_name_plural': 'Indicators of Change'},
        ),
        migrations.AlterModelOptions(
            name='communityactivity',
            options={'ordering': ['related_collaborative', 'related_goal', 'related_objective', 'related_strategy', 'activity_status', 'completedby_year'], 'verbose_name': 'Community Activities', 'verbose_name_plural': 'Community Activity'},
        ),
        migrations.AlterModelOptions(
            name='communitycollaborative',
            options={'ordering': ('community_collab_name',), 'verbose_name': 'Community Collaborative', 'verbose_name_plural': 'Community Collaboratives'},
        ),
        migrations.AlterModelOptions(
            name='dhhspriority',
            options={'ordering': ('related_goal',), 'verbose_name': 'DHHS Priority', 'verbose_name_plural': 'DHHS Priorities'},
        ),
        migrations.AlterModelOptions(
            name='goal',
            options={'ordering': ('goal_number',), 'verbose_name': 'Goal', 'verbose_name_plural': 'Goals'},
        ),
        migrations.AlterModelOptions(
            name='ncffteam',
            options={'ordering': ('ncff_team_name',), 'verbose_name': 'NCFF Initiative / Team / Priority Area', 'verbose_name_plural': 'NCFF Initiatives / Teams / Priority Areas'},
        ),
        migrations.AlterModelOptions(
            name='objective',
            options={'ordering': ('related_goal', 'objective_number'), 'verbose_name': 'Objective', 'verbose_name_plural': 'Objectives'},
        ),
        migrations.AlterModelOptions(
            name='performancemeasure',
            options={'ordering': ('measure',), 'verbose_name': 'Performance Measure', 'verbose_name_plural': 'Performance Measures'},
        ),
        migrations.AlterModelOptions(
            name='strategy',
            options={'ordering': ('related_goal', 'related_objective', 'strategy_number'), 'verbose_name': 'Strategy', 'verbose_name_plural': 'Strategies'},
        ),
        migrations.AlterModelOptions(
            name='strategyactivity',
            options={'ordering': ['related_goal', 'related_objective', 'related_strategy', 'activity_number', 'completedby_year'], 'verbose_name': 'Strategy Activity', 'verbose_name_plural': 'Strategy Activities'},
        ),
        migrations.AlterModelOptions(
            name='strategypriority',
            options={'ordering': ['community_collab', 'strategy'], 'verbose_name': 'Community Collab Priority', 'verbose_name_plural': 'Community Collab Priorities'},
        ),
        migrations.AddField(
            model_name='communitycollaborative',
            name='community_collab_short_name',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='ncffteam',
            name='ncff_team_short_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterModelTable(
            name='activitystatus',
            table='activity_statuses',
        ),
        migrations.AlterModelTable(
            name='changeindicator',
            table='change_indicator',
        ),
        migrations.AlterModelTable(
            name='communityactivity',
            table='community_activity',
        ),
        migrations.AlterModelTable(
            name='communitycollaborative',
            table='community_collab',
        ),
        migrations.AlterModelTable(
            name='dhhspriority',
            table='dhhs_priority',
        ),
        migrations.AlterModelTable(
            name='goal',
            table='goal',
        ),
        migrations.AlterModelTable(
            name='ncffteam',
            table='ncff_team',
        ),
        migrations.AlterModelTable(
            name='objective',
            table='objective',
        ),
        migrations.AlterModelTable(
            name='performancemeasure',
            table='performance_measure',
        ),
        migrations.AlterModelTable(
            name='strategy',
            table='strategy',
        ),
        migrations.AlterModelTable(
            name='strategyactivity',
            table='strategy_activity',
        ),
        migrations.AlterModelTable(
            name='strategypriority',
            table='collab_strategy_priority',
        ),
    ]
