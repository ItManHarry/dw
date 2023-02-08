from django.contrib import admin

# Register your models here.
from . models import BizQuestion, BizChoice
class ChoiceInline(admin.TabularInline):
    model = BizChoice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question Content', {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
admin.site.register(BizQuestion, QuestionAdmin)
# admin.site.register(BizQuestion)
# admin.site.register(BizChoice)
