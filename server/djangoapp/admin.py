from django.contrib import admin
from .models import CarMake, CarModel

# CarModelInline class to display CarModel inline within CarMake admin
 class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1


# CarModelAdmin class to customize the admin interface for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'year', 'car_make']
    list_filter = ['type', 'year', 'car_make']
    search_fields = ['name', 'car_make__name']



class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    search_fields = ['name']


# Registering models with their respective admins
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
