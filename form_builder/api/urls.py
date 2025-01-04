from django.urls import path
from .views import FormView, SubmitResponseView, AnalyticsView, FormDetailView, GetResponsesView

urlpatterns = [
    path('forms/', FormView.as_view(), name='form-list'),
    path('form-detail/<int:form_id>/', FormDetailView.as_view(), name='form-detail' ),
    path('forms/<int:form_id>/', SubmitResponseView.as_view(), name='submit-response'),
    path('forms/<int:form_id>/responses/', GetResponsesView.as_view(), name='get-responses'),
    path('forms/<int:form_id>/analytics/', AnalyticsView.as_view(), name='form-analytics'),
]
