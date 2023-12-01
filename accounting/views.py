from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import Transaction, FinancialEntity
from django.utils import timezone
from datetime import timedelta
from urllib.parse import quote
import math


class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        transaction = Transaction.objects.get(id=id)

        data = {
            'service': transaction.service,
            'date_time_transacion': transaction.date_time_transaction,
            'title': transaction.title,
            'amount': transaction.amount,
            'receipt_number': transaction.receipt_number,
            'origin_name': transaction.origin_name,
            'origin_account': transaction.origin_account,
            'origin_finantial_entity': transaction.origin_financial_entity.name,
            'registered_by': transaction.registered_by.first_name + ' ' + transaction.registered_by.last_name,
            'date_time_registered': transaction.date_time_registered
        }

        return Response(data, status=status.HTTP_200_OK)


class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        period = request.query_params.get('period', None)
        service = request.query_params.get('service', None)
        page = request.query_params.get('page', None);

        if period:
            today = timezone.now()
            if period == '7':
                start_date = today - timedelta(days=7)
            elif period == '15':
                start_date = today - timedelta(days=15)
            elif period == '30':
                start_date = today - timedelta(days=30)
            elif period == '60':
                start_date = today - timedelta(days=60)
            elif period == '90':
                start_date = today - timedelta(days=90)
            else:
                start_date = today - timedelta(days=7)  
            
            queryset = Transaction.objects.filter(date_time_transaction__gte=start_date)
        else:
            queryset = Transaction.objects.all()

        if service:
            queryset = queryset.filter(service=service)

        PAGE_SIZE = 8

        previous = None
        next = None
        url = '/api/accounting/transactions/'

        total_pages = math.ceil(len(queryset) / PAGE_SIZE)

        if page:
            page = int(page)
            end = PAGE_SIZE * page
            start = end - PAGE_SIZE
            queryset = queryset.order_by('-date_time_transaction')[start: end]

            if page > 1:
                previous = url + '?page=' + str(page - 1)

            if  total_pages != 0 and total_pages != page:
                next = url + '?page=' + str(page + 1)
                
            if next:
                next = next + '&period='+period
            if previous:
                previous = previous + '&period='+period

            if service:
                if next:
                    next = next + '&service='+quote(service)
                if previous:
                    previous = previous + '&service='+quote(service)
           
        queryset = [
            {
                'attributes' : {
                    'id': transaction.id,
                    'service': transaction.service,
                    'date_time_transaction': transaction.date_time_transaction,
                    'amount': transaction.amount,
                    'origin_financial_entity': transaction.origin_financial_entity.name
                }, 
                'links': {
                    'self': url + str(transaction.id) + '/'
                }
            }
            for transaction in queryset
        ]

        data = {
            'meta': {
                'total_pages': total_pages,
                'count': len(queryset),
                'next': next,
                'previous': previous
            },
            'data': queryset
        }
        return Response(data, status=status.HTTP_200_OK)
   
    def post(self, request, *args, **kwargs):
        date_time_transaction = request.data.get('date_time_transaction')
        amount = request.data.get('amount')
        origin_financial_entity = request.data.get('origin_financial_entity')

        if not date_time_transaction or not amount or not origin_financial_entity:
            return Response({'error': 'missing fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction = Transaction.objects.create(
            date_time_transaction = date_time_transaction,
            title = request.data.get('title', ''),
            amount = amount,
            receipt_number = request.data.get('receipt_number', ''),
            origin_name = request.data.get('origin_name', ''),
            origin_account = request.data.get('origin_account', ''),
            origin_financial_entity = FinancialEntity.objects.get(id=int(origin_financial_entity)),
            destination_name = 'JAZMÍN VALDEZ',
            destination_account = '087436091',
            destination_financial_entity = FinancialEntity.objects.get(name='BANCO ITAU PARAGUAY S.A.'),
            registered_by = User.objects.get(id=request.user.id)
        )

        service = 'Transferencias Otros Bancos'
        if transaction.destination_financial_entity.id == transaction.origin_financial_entity.id:
            service = 'Transferencias Internas'

        transaction.service = service
        transaction.save()

        return Response({'id': transaction.id}, status=status.HTTP_201_CREATED)
    
    
    
class FinancialEntityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        financial_entities = FinancialEntity.objects.all()
        
        data = [
            {
                'id': entity.id,
                'name': entity.name,
            }
            for entity in financial_entities
        ]

        return Response(data, status=status.HTTP_200_OK)
        


