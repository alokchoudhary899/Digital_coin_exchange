from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import Transaction
from django.contrib.auth.models import User
from coinexchange.serializers import TransactionSerializer


@csrf_exempt
def add_transaction(request):
    if request.method == 'POST':
        received_json = json.loads(request.body)
        transaction_keys = ['sender', 'receiver', 'amount','time']
        if not all(key in received_json for key in transaction_keys):
            return 'Some elements of the transaction are missing', HttpResponse(status=400)
        receiver = User.objects.get(username=received_json['receiver'])
        current_sender_amount = User.objects.filter(id=int(received_json['sender'])).values('amount')[0]['amount']
        current_receiver_amount = User.objects.filter(username=received_json['receiver']).values('amount')[0]['amount']

        if current_sender_amount >= int(received_json['amount']):
            if receiver:
                sender = User.objects.get(id=int(received_json['sender']))
                transaction_obj = Transaction.objects.create(sender=sender,
                                                             receiver=receiver,
                                                             amount=received_json['amount'],
                                                            )
                update_sender_amount = User.objects.filter(id=int(received_json['sender'])).update(amount= current_sender_amount - int(received_json['amount']))
                update_receiver_amount = User.objects.filter(username=received_json['receiver']).update(amount= current_receiver_amount + int(received_json['amount']))
                response = {'message': f'This transaction will be added to Account'}
                return JsonResponse(response)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Fail": "Not enough Balance"})


class TransactionAPIView(APIView):
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        t_list = Transaction.objects.filter(sender_id=self.request.user.id)
        serializer = self.serializer_class(t_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckBalanceAPIView(APIView):

    def get(self, request, *args, **kwargs):
        current_balance = User.objects.filter(id=self.request.user.id).values('amount')[0]['amount']
        return Response({'balance' : current_balance})
