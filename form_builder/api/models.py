from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class AdminUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Form(models.Model):
    form_name = models.CharField(max_length=200, null=False, default='Default Form') 
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.form_name

    def save(self, *args, **kwargs):
        max_rows = 100  
        if Form.objects.count() >= max_rows:
            raise ValidationError(f"Cannot add more than {max_rows} rows.")
        super().save(*args, **kwargs)



class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text'),
        ('dropdown', 'Dropdown'),
        ('checkbox', 'Checkbox'),
    ]

    form = models.ForeignKey(Form, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='text') 
    question_text = models.CharField(max_length=255, null=True)  
    options = models.TextField(null=True, blank=True)  
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.question_text


class FormResponse(models.Model):
    form = models.ForeignKey(Form, related_name='responses', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    questions = models.ManyToManyField(Question)
  

class Answer(models.Model):
    response = models.ForeignKey(FormResponse, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer_text = models.TextField(default="")

