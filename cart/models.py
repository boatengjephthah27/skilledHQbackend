from django.db import models
import uuid
from core.utils.constants import SERVICE, WORKING_OPTIONS, WORKING_HOURS, REMOTE, ORDER_TYPE, PROJECT_TYPE, START_TIME, DURATION_NEED, ORDER_STATUS
from users.models import CustomUser

# Create your models here.


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    order_type = models.CharField(
        max_length=20, choices=ORDER_TYPE, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.organization.capitalize()} ({self.email.capitalize()})"


class Cart(models.Model):
    id = models.AutoField(primary_key=True),
    service = models.CharField(
        max_length=60, choices=SERVICE, default='Engineering')
    service_id = models.IntegerField(null=True, blank=True)
    number_needed = models.IntegerField(null=True, blank=True, default=1)
    role_description = models.TextField(null=True, blank=True)
    working_hours = models.CharField(
        choices=WORKING_HOURS, default='60', null=True, blank=True)
    service_role = models.CharField(max_length=100, null=True, blank=True)
    remote = models.CharField(
        max_length=60, choices=REMOTE, default='Yes', null=True, blank=True)
    working_options = models.CharField(
        max_length=60, choices=WORKING_OPTIONS, default='Full Time (FT)', null=True, blank=True)
    project_type = models.CharField(
        max_length=100, choices=PROJECT_TYPE, default='New Project', null=True, blank=True)
    duration_of_hire = models.CharField(
        max_length=100, choices=DURATION_NEED, default='Less than 1 week', null=True, blank=True)
    talent_start_time = models.CharField(
        max_length=100, choices=START_TIME, default='Immediately', null=True, blank=True)
    unlisted_service_role = models.CharField(
        max_length=255, null=True, blank=True)
    role_description_file = models.FileField(
        upload_to='role_description_files/', null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        organization = self.order.organization
        date = self.order.date
        return f" #{self.service.capitalize()}  -  [{organization.capitalize()}]  .........  ( {date.day} -  {date.month} -  {date.year} )"


class Skill(models.Model):
    id = models.AutoField(primary_key=True),
    skill = models.CharField(max_length=100, null=True, blank=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, related_name='required_skill')

    def __str__(self):
        organization = self.cart.order.organization
        service_role = self.cart.service_role
        return f"{self.skill}   -   {service_role.capitalize()}"
