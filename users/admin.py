from django.contrib import admin
from .models import CustomUser, Organization, Address, Talent,  Degree, Project, TechnologiesUsed, Manager, SkillStack, Language, Social, Experience, Challenge, IdentityFiles
from nested_admin import NestedModelAdmin, NestedStackedInline
# Register your models here.


# class SkillModelInline(NestedStackedInline):
#     model = Skill
#     extra = 1


class DegreeModelInline(NestedStackedInline):
    model = Degree
    # inlines = [SkillModelInline]
    extra = 1


class TechnologiesUsedModelInline(NestedStackedInline):
    model = TechnologiesUsed
    # inlines = [SkillModelInline]
    extra = 1


class ProjectModelInline(NestedStackedInline):
    model = Project
    inlines = [TechnologiesUsedModelInline]
    extra = 1


class TalentAdmin(NestedModelAdmin):
    inlines = [DegreeModelInline, ProjectModelInline]
    search_fields = ['role', 'rate_per_hour',
                     'full_time_hours', 'part_time_hours', 'verified', 'years_experience', 'remote', 'user']
    list_display = ['user', 'role', 'rate_per_hour',
                    'full_time_hours', 'part_time_hours', 'verified', 'years_experience', 'remote', ]


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'gender',
                     'first_name', 'last_name', 'is_active', 'is_client', 'contact']
    list_display = ['email', 'gender',
                    'first_name', 'last_name', 'is_active', 'is_client', 'contact']


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Organization)
admin.site.register(Address)
admin.site.register(Talent, TalentAdmin)
admin.site.register(Degree)
admin.site.register(Project)
admin.site.register(TechnologiesUsed)
admin.site.register(Manager)
admin.site.register(SkillStack)
admin.site.register(Language)
admin.site.register(Social)
admin.site.register(Experience)
admin.site.register(Challenge)
admin.site.register(IdentityFiles)
