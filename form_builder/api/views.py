from django.shortcuts import render
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Form, Question, FormResponse, Answer
from .serializers import FormSerializer, QuestionSerializer, ResponseSerializer, FormResponseSerializer
from django.db import transaction

class FormView(APIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Form.objects.all()
    
    def get(self, request):
        forms = self.get_queryset()
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)


    
class FormDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly] 
    def get(self, request, form_id):
        try:
    
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return Response({"detail": "Form not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
        questions = form.questions.all()
        
 
        question_data = QuestionSerializer(questions, many=True).data
        return Response({
            "form_title": form.form_name,
            "questions": question_data
        }, status=status.HTTP_200_OK)
    

class SubmitResponseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return Response({"detail": "Form not found."}, status=status.HTTP_404_NOT_FOUND)
             
        form_response = FormResponse.objects.create(form=form)
         

        for response in request.data.get('responses', []):
            question_id = response.get('question_id')
            answer_text = response.get('answer')

            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return Response({"detail": f"Question with ID {question_id} not found."}, status=status.HTTP_404_NOT_FOUND)

           
            Answer.objects.create(response=form_response, question=question, answer_text=answer_text)


        response_data = ResponseSerializer(form_response).data
        return Response({"message": "Response submitted successfully.", "response": response_data}, status=status.HTTP_200_OK)


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)

        except Form.DoesNotExist:
            return Response({"detail": "Form Not Found"}, status=status.HTTP_404_NOT_FOUND)

        analytics = {
            "total_responses": FormResponse.objects.filter(form=form).count(),
            "question_analytics": [],
        }

        for question in form.questions.all():
            answers = Answer.objects.filter(question=question)
            if question.question_type == 'text':
                word_count = {}
                for ans in answers:
                    for word in ans.answer_text.split():
                        if len(word) >= 5:  
                            word_count[word] = word_count.get(word, 0) + 1
                top_words = sorted(word_count.items(), key=lambda x: -x[1])[:5]
                analytics["question_analytics"].append({
                    "question": question.question_text,
                    "top_words": top_words,
                })
            elif question.question_type == 'checkbox':
                option_combinations = {}
                for ans in answers:
                    selected_options = ans.answer_text.split(',')
                    selected_options = sorted(selected_options)  
                    combination = ','.join(selected_options)
                    option_combinations[combination] = option_combinations.get(combination, 0) + 1
                top_combinations = sorted(option_combinations.items(), key=lambda x: -x[1])[:5]
                analytics["question_analytics"].append({
                    "question": question.question_text,
                    "top_combinations": top_combinations,
                })
            elif question.question_type == 'dropdown':
                option_counts = {}
                for ans in answers:
                    selected_option = ans.answer_text
                    option_counts[selected_option] = option_counts.get(selected_option, 0) + 1
                top_options = sorted(option_counts.items(), key=lambda x: -x[1])[:5]
                analytics["question_analytics"].append({
                    "question": question.question_text,
                    "top_options": top_options,
                })
        return Response(analytics)


class GetResponsesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return Response({"detail": "Form not found."}, status=status.HTTP_404_NOT_FOUND)

        responses = FormResponse.objects.filter(form=form)


        responses = responses.prefetch_related('questions', 'answers')

     
        response_data = FormResponseSerializer(responses, many=True).data

        return Response({"responses": response_data}, status=status.HTTP_200_OK)
    
    
class CreateFormView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            form = serializer.save()
            return Response({
                "message": "Form created successfully.",
                "form": FormSerializer(form).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddQuestionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return Response({"detail": "Form not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
     
            question = serializer.save(form=form)
            return Response({
                "message": "Question added successfully.",
                "question": QuestionSerializer(question).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
