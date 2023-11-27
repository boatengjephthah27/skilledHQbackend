from django.shortcuts import render
from rest_framework import viewsets, views, generics
from rest_framework.permissions import AllowAny
from .models import Contract, Billing, TalentApplication, SuggestedContract, Message, ContractChangeRequest, Responsibility, Qualification, RoleDescription
from .serializers import ContractSerializer, SuggestedContractSerializer, TalentApplicationSerializer, ContractChangeRequestSerializer, MessageSerializer, AdminMessageSerializer, ResponsibilitySerializer, QualificationSerializer, RoleDescriptionSerializer, BillingSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated


# Create your views here.
class ContractViewsets(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractListViewsets(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Contract.objects.all().order_by('-status')
    serializer_class = ContractSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            client = Contract.objects.filter(client_ID=user_id)
            if not client:
                talent = Contract.objects.filter(talent_ID=user_id)
                return talent
            return client

        return Contract.objects.none()


class SuggestedContractViewsets(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = SuggestedContract.objects.all()
    serializer_class = SuggestedContractSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            client = SuggestedContract.objects.filter(client_ID=user_id)
            return client

        return SuggestedContract.objects.none()


class SuggestedContractViews(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = SuggestedContract.objects.all()
    serializer_class = SuggestedContractSerializer


class ResponsibilityViewsets(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer


class QualificationViewsets(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class RoleDescriptionViewsets(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = RoleDescription.objects.all()
    serializer_class = RoleDescriptionSerializer


class TalentApplicationViewsets(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny,]
    queryset = TalentApplication.objects.all()
    serializer_class = TalentApplicationSerializer

    def post(self, request, format=None):
        serializer = TalentApplicationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # TODO Send a message to Slack and to Admin Email

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = AdminMessageSerializer
    permission_classes = [AllowAny,]


class ContractChangeRequestView(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = ContractChangeRequest.objects.all()
    serializer_class = ContractChangeRequestSerializer
    permission_classes = [AllowAny,]


class MessageDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class BillingViewsets(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        if user:
            bills = Billing.objects.filter(client=user)
            if not bills:
                bills = Billing.objects.filter(talent=user)
            return bills

        return Billing.objects.none()


class MarkMessageAsReadView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny,]

    def partial_update(self, request, *args, **kwargs):
        message = self.get_object()
        user_id = request.data.get('user_id')

        if user_id not in message.read_by.all():
            message.read_by.add(user_id)
            message.save()
            return Response({'Message marked as read.'}, status=status.HTTP_200_OK)
        else:
            return Response({'Message is already marked as read.'}, status=status.HTTP_400_BAD_REQUEST)
