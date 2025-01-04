from django.contrib import admin
from .models import Form, Question, Answer, FormResponse
from django import forms

class QuestionAdminForm(forms.ModelForm):
    options_list = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="Enter one option per line. Only required for dropdown and checkbox questions."
    )

    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.options:
            self.fields['options_list'].initial = self.instance.options

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')
        options_list = cleaned_data.get('options_list')

        if question_type in ['dropdown', 'checkbox']:
            if not options_list:
                raise forms.ValidationError(
                    "Options are required for dropdown and checkbox questions."
                )
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.question_type in ['dropdown', 'checkbox']:
            instance.options = self.cleaned_data['options_list']
        else:
            instance.options = None
        if commit:
            instance.save()
        return instance

class QuestionInline(admin.TabularInline):
    model = Question
    form = QuestionAdminForm
    extra = 1
    fields = ('question_type', 'question_text', 'options_list', 'order')

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('id', 'form', 'question_type', 'question_text', 'get_options')
    list_filter = ('question_type',)
    
    def get_options(self, obj):
        if obj.options:
            return obj.options.replace('\n', ', ')
        return '-'
    get_options.short_description = 'Options'


class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_name', 'created_at',)
    search_fields = ('form_name',)
    list_filter = ('created_at',)
    inlines = [QuestionInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ['question', 'answer_text']
    extra = 0

class FormResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'submitted_at')
    search_fields = ['form__form_name', 'submitted_at']
    list_filter = ['form']
    inlines = [AnswerInline]

admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(FormResponse, FormResponseAdmin)