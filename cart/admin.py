from django.contrib import admin
from .models import Cart, Order, Skill
from nested_admin import NestedModelAdmin, NestedStackedInline


# Register your models here.


class SkillModelInline(admin.StackedInline):
    model = Skill
    extra = 1  # Number of empty forms to display


class CartAdmin(admin.ModelAdmin):
    inlines = [SkillModelInline]

    search_fields = ['service', 'service_role',
                     'working_hours', 'remote', 'working_options', 'number_needed']
    list_display = ['service', 'service_role',
                    'working_hours', 'working_options', 'remote', 'number_needed', 'order', 'skill']

    def skill(self, obj):
        return obj.required_skill


class SkillAdmin(admin.ModelAdmin):
    search_fields = ['skill']
    list_display = ['skill', 'cart']

    def cart(self, obj):
        return obj.cart.service


class SkillModelInline(NestedStackedInline):
    model = Skill
    extra = 1


class CartModelInline(NestedStackedInline):
    model = Cart
    inlines = [SkillModelInline]
    extra = 1


class OrderAdmin(NestedModelAdmin):
    inlines = [CartModelInline]
    search_fields = ['full_name', 'organization',
                     'contact', 'email', 'order_type', 'status']
    list_display = ['full_name', 'organization',
                    'contact', 'email', 'order_type', 'status']


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Skill, SkillAdmin)
