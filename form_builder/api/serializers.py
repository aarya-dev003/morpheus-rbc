from rest_framework import serializers
from .models import Form, Question, FormResponse, Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'options', 'order']



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'response', 'question', 'answer_text']


class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many = True)
    class Meta:
        model = FormResponse
        fields =  '__all__' #['id', 'form', 'submitted_at']


class FormResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many = True)
    class Meta:
        model = Form
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'