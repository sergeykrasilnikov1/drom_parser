from django.contrib import admin
from .models import Car, Complectation

class ComplectationInline(admin.TabularInline):
    model = Complectation
    extra = 0
    fields = ('name', 'volume', 'fuel_type', 'power', 'transmission', 'drive', 'price', 'year')
    readonly_fields = ('volume', 'fuel_type', 'power', 'transmission', 'drive', 'price', 'year')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'model_url', 'image_url')
    search_fields = ('model',)
    inlines = [ComplectationInline]

@admin.register(Complectation)
class ComplectationAdmin(admin.ModelAdmin):
    list_display = ('name', 'car', 'volume', 'fuel_type', 'power', 'transmission', 'drive', 'price', 'year')
    list_filter = ('car', 'fuel_type', 'transmission', 'drive')
    search_fields = ('name', 'car__model')
