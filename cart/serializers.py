from rest_framework import serializers
from .models import Cart, Order, Skill
from users.serializers import CustomUserSerializer


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", 'skill']


class CartSerializer(serializers.ModelSerializer):
    required_skill = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [field.name for field in Cart._meta.fields] + \
            ['required_skill']


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
