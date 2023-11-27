from rest_framework import serializers
from .models import Contract, TalentApplication, SuggestedContract, Message, ContractChangeRequest, Responsibility, Qualification, Billing, RoleDescription
from cart.serializers import OrderSerializer
from users.serializers import CustomUserSomeSerializer, CustomUserTalentSerializer


class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = '__all__'


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'


class RoleDescriptionSerializer(serializers.ModelSerializer):
    responsibility = ResponsibilitySerializer(many=True, read_only=True)
    qualification = QualificationSerializer(many=True, read_only=True)
    order_ID = OrderSerializer(many=False, read_only=True)

    class Meta:
        model = RoleDescription
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    role_description = RoleDescriptionSerializer(many=False, read_only=True)
    client_ID = CustomUserSomeSerializer(many=False, read_only=True)
    talent_ID = CustomUserTalentSerializer(many=False, read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class TalentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentApplication
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ContractChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractChangeRequest
        fields = '__all__'


class SuggestedContractSerializer(serializers.ModelSerializer):
    client_ID = CustomUserSomeSerializer(many=False, read_only=True)
    talent_ID = CustomUserTalentSerializer(many=False, read_only=True)
    order_ID = OrderSerializer(many=False, read_only=True)

    class Meta:
        model = SuggestedContract
        fields = '__all__'


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'


class AdminMessageSerializer(MessageSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('read_by',)
