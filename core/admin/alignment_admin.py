from django.contrib import admin


class ChangeIndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator', 'related_goal')
    search_fields = ('indicator',)

    def get_goal_number(self, obj):
        return obj.related_goal.goal_number
    get_goal_number.short_description = 'Goal Number'


class PerformanceMeasureAdmin(admin.ModelAdmin):
    list_display = ('measure', 'related_goal')
    search_fields = ('measure',)

    def get_goal_number(self, obj):
        return obj.related_goal.goal_number
    get_goal_number.short_description = 'Goal Number'
