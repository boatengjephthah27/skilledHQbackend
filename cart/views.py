from django.shortcuts import render
from django.http import QueryDict
from rest_framework import viewsets, status
from .serializers import OrderSerializer, CartSerializer, SkillSerializer
from .models import Order, Cart, Skill
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from users.models import CustomUser
import re
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from django.conf import settings
import os


def send_order_mail(client_email):

    subject = 'New Order Email - SkilledHQ'

    admin_email = os.environ.get('EMAIL')

    html_message = render_to_string(
        'email.html', {'client_email': client_email})
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=admin_email,
        to=['jboateng@skilledhq.com']
    )

    message.attach_alternative(html_message, 'text/html')
    ok = message.send()


class OrderViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny,]
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer

    def get_queryset(self, request):
        client_id = self.request.query_params.get('client_id')
        if client_id:
            client_orders = Order.objects.filter(user=client_id)

            return client_orders

        return Order.objects.none()

    def _querydict_to_dict(self, query_dict):
        def clean_key_value(key, value):
            if "\n" in key:
                key = key.strip("\n")
            if "\n" in value:
                value = value.strip("\n")
            return key, value

        def process_key(keys, obj, value):
            if keys:
                key = keys[0]
                rest_keys = keys[1:]

                if key.isdigit():
                    key = int(key)

                if isinstance(obj, list):
                    if key >= len(obj):
                        obj.extend([{}] * (key - len(obj) + 1))
                    if not obj[key]:
                        obj[key] = {} if rest_keys else ""
                    process_key(rest_keys, obj[key], value)

                elif isinstance(obj, dict):
                    if key not in obj:
                        obj[key] = {} if rest_keys else value
                    process_key(rest_keys, obj[key], value)

        result = {}
        for key, value in query_dict.dict().items():
            key, value = clean_key_value(key, query_dict.get(key))
            keys = (re.split(r'\[|\]', key))[:-1]
            keys = [key for key in keys if key]
            process_key(keys, result, value)

        return result

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        data: QueryDict = self._querydict_to_dict(request.data)

        try:
            user_id = request.data.get('user')
            if user_id != "":
                user_instance = CustomUser.objects.get(id=user_id)
                order_data = {
                    'email': request.data['email'],
                    'full_name': request.data['full_name'],
                    'organization': request.data['organization'],
                    'additional_info': request.data['additional_info'],
                    'contact': request.data['contact'],
                    'order_type': request.data['order_type'],
                    'status': "Pending",
                    'user': user_instance.id,
                }
            else:
                order_data = {
                    'email': request.data['email'],
                    'full_name': request.data['full_name'],
                    'organization': request.data['organization'],
                    'additional_info': request.data['additional_info'],
                    'status': "Pending",
                    'contact': request.data['contact'],
                    'contact': request.data['contact'],
                    'user': None,
                }
            serialized_order = self.get_serializer(data=order_data)
            serialized_order.is_valid(raise_exception=True)
            new_order = serialized_order.save()

            cart_data = data.get('cart', {})
            for _, item in cart_data.items():
                cart = Cart.objects.create(
                    service=item.get('service'),
                    service_id=item.get('service_id'),
                    number_needed=item.get('number_needed'),
                    role_description=item.get('role_description'),
                    working_hours=item.get('working_hours'),
                    service_role=item.get('service_role'),
                    remote=item.get('remote'),
                    project_type=item.get('project_type'),
                    duration_of_hire=item.get('talent_need_duration'),
                    talent_start_time=item.get('talent_start_time'),
                    working_options=item.get('working_option', ),
                    unlisted_service_role=item.get('unlisted_service_role'),
                    role_description_file=item.get('role_description_file'),
                    order=new_order
                )

                skills_data = item.get('required_skill', {})
                for _, skill in skills_data.items():
                    Skill.objects.create(skill=skill, cart=cart)

            client_email = request.data['email']

            # TODO Run a background funciton to Send a message to Slack and to Admin Email

            send_order_mail(client_email)

            return Response("Data saved successfully", status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
