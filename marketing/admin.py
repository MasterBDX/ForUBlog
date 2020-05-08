from django.contrib import admin
from .models import MarketingPrefrence

class MarketingPrefrenceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated']
    readonly_fields = ['timestamp', 'updated','mailchimp_msg']

    class Meta:
        model = MarketingPrefrence
        fields = '__all__'

admin.site.register(MarketingPrefrence, MarketingPrefrenceAdmin)
