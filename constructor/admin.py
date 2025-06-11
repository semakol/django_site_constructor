from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(SampleUser)
class SampleUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'relation', 'sample_id', 'user_id_id',)
    search_fields = ('user__username',)
    list_filter = ('relation',)


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state', 'image', 'is_template', 'user_id')
    list_filter = ('state', )

    def user_id(self, obj):
        user = User.objects.filter(sampleuser__sample=obj, sampleuser__relation='creator').first()
        return user
