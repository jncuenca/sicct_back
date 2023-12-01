from django.urls import path
from .views import FinancialEntityView, TransactionView, TransactionDetailView

urlpatterns = [
    path('transactions/', TransactionView.as_view()),
    path('financial_entities/', FinancialEntityView.as_view()),
    path('transactions/<int:id>/', TransactionDetailView.as_view()),
]