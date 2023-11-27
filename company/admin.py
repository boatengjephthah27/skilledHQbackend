from django.contrib import admin
from .models import Contract, TalentApplication, Message, Responsibility, Qualification, RoleDescription, Billing, ContractChangeRequest, SuggestedContract
from nested_admin import NestedModelAdmin, NestedStackedInline

# Register your models here.


class BillingAdmin(admin.ModelAdmin):
    search_fields = ['service', 'date', 'amount', 'client__first_name',
                     'client__last_name', 'talent__first_name', 'talent__last_name']
    list_display = ['service', 'date', 'amount', 'client',
                    'talent',]


class TalentApplicationAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'contact', 'email',
                     'expertise', 'expertise_unlisted', 'remote']
    list_display = ['first_name', 'last_name', 'contact', 'email',
                    'expertise', 'expertise_unlisted', 'remote']


class QualificationInline(NestedStackedInline):
    model = Qualification
    extra = 1


class ResponsibilityInline(NestedStackedInline):
    model = Responsibility
    extra = 1


class ContractAdmin(NestedModelAdmin):
    # inlines = [ResponsibilityInline, QualificationInline]
    search_fields = ['service', 'start_date', 'end_date', 'working_hours_per_week', 'client__first_name',
                     'client__last_name', 'talent__first_name', 'talent__last_name', 'hourly_rate', 'remote']
    list_display = ['service', 'role',
                    'start_date', 'end_date', 'type', 'status']


class RoleDescriptionAdmin(NestedModelAdmin):
    inlines = [ResponsibilityInline, QualificationInline]
    search_fields = ['description', 'responsibility__description',
                     'qualification__description',]
    list_display = ['description', ]


# class SkillModelInline(NestedStackedInline):
#     model = Skill
#     extra = 1


# class CartModelInline(NestedStackedInline):
#     model = Cart
#     inlines = [SkillModelInline]
#     extra = 1


# class OrderAdmin(NestedModelAdmin):
#     inlines = [CartModelInline]
#     search_fields = ['full_name', 'organization',
#                      'contact', 'email', 'order_type', 'status']
#     list_display = ['full_name', 'organization',
#                     'contact', 'email', 'order_type', 'status']


# admin.site.register(Order, OrderAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractChangeRequest)
admin.site.register(TalentApplication, TalentApplicationAdmin)
admin.site.register(Message)
admin.site.register(Responsibility)
admin.site.register(Qualification)
admin.site.register(RoleDescription, RoleDescriptionAdmin)
admin.site.register(Billing, BillingAdmin)
admin.site.register(SuggestedContract)
