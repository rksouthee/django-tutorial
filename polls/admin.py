"""admin"""
from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(
    admin.TabularInline[Choice]
):  # pylint: disable=unsubscriptable-object,too-few-public-methods
    """ChoiceInline"""

    model = Choice
    extra = 3


class QuestionAdmin(
    admin.ModelAdmin[Question]
):  # pylint: disable=unsubscriptable-object,too-few-public-methods
    """QuestionAdmin"""

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inline = [ChoiceInline]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
