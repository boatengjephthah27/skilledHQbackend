from django.db import models
import uuid
from users.models import CustomUser
from cart.models import Order
from core.utils.constants import CONTRACT_STATUS, SERVICE, START_WORK, WORKING_OPTIONS, REMOTE, SERVICE_EXPERTISE

# Create your models here.


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_ID = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='contract_client')
    talent_ID = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='contract_talent',  null=True, blank=True)
    service = models.CharField(
        max_length=20, choices=SERVICE, null=True, blank=True)
    role = models.CharField(
        max_length=50,  null=True, blank=True)
    type = models.CharField(
        max_length=50, choices=CONTRACT_STATUS, null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=(('Active', 'Active'), ('Inactive', 'Inactive')), null=True, blank=True)
    remote = models.CharField(
        max_length=50, choices=(('Yes', 'Yes'), ('No', 'No')), null=True, blank=True)
    start_date = models.DateTimeField(max_length=255, null=True, blank=True)
    end_date = models.DateTimeField(max_length=255, null=True, blank=True)
    working_hours_per_week = models.IntegerField(null=True, blank=True)
    hourly_rate = models.IntegerField(null=True, blank=True)
    role_description_file = models.FileField(
        upload_to='role_description_files/', null=True, blank=True)
    role_description = models.ForeignKey(
        "RoleDescription", on_delete=models.CASCADE, null=True, blank=True)
    contract_file = models.FileField(
        upload_to='contracts/', null=True, blank=True)

    def __str__(self):
        organization = self.client_ID.organization.all().first()
        return f"{organization.name.capitalize()} ----- {self.talent_ID.first_name.capitalize()} {self.talent_ID.last_name.capitalize()} ***** Contract"


class Responsibility(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    role = models.ForeignKey(
        "RoleDescription", on_delete=models.CASCADE, null=True, blank=True, related_name='responsibility')

    def __str__(self) -> str:
        return f"{self.description}"


class Qualification(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    role = models.ForeignKey(
        "RoleDescription", on_delete=models.CASCADE, null=True, blank=True, related_name='qualification')


class RoleDescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_ID = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_id',  null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        order = self.order_ID
        return f"{order}"


class TalentApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    service = models.CharField(
        max_length=255, choices=SERVICE, null=True, blank=True)
    expertise = models.CharField(
        choices=SERVICE_EXPERTISE, max_length=255, null=True, blank=True)
    expertise_unlisted = models.CharField(
        max_length=255, null=True, blank=True)
    plan_to_start_work = models.CharField(
        max_length=30, choices=START_WORK, null=True, blank=True)
    time_commitment = models.CharField(
        max_length=20, choices=WORKING_OPTIONS, null=True, blank=True)
    remote = models.CharField(
        max_length=20, choices=REMOTE, null=True, blank=True)
    in_office = models.CharField(
        max_length=20, choices=REMOTE, null=True, blank=True)
    resume = models.FileField(upload_to='resume/', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.first_name}   -   {self.expertise}"


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    read_by = models.ManyToManyField(
        CustomUser, related_name='read_messages', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Billing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.CharField(
        max_length=20, choices=SERVICE, null=True, blank=True)
    title = models.CharField(max_length=355, null=True, blank=True)
    client = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='billing_client')
    talent = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='billing_talent')
    date = models.DateTimeField(auto_now_add=True)
    receipt = models.FileField(
        upload_to='billing_receipts/',  null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        organization = self.client.organization.all().first()
        return f"{self.amount}   -   {organization.name.capitalize()}  -  {self.talent.first_name.capitalize()} {self.talent.last_name.capitalize()}    ( {self.date.day} -  {self.date.month} -  {self.date.year} )"


class ContractChangeRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name='contract')
    service = models.CharField(
        max_length=20, choices=SERVICE, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.contract.client_ID.first_name} {self.contract.client_ID.last_name}   -   {self.contract.talent_ID.first_name} {self.contract.talent_ID.first_name}   [CHANGE]"


class SuggestedContract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_ID = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='client')
    talent_ID = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='talent_suggested',  null=True, blank=True)
    order_ID = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order',  null=True, blank=True)
    service = models.CharField(
        max_length=20, choices=SERVICE, null=True, blank=True)
    role = models.CharField(
        max_length=50,  null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=(('Awaiting Response', 'Awaiting Response'), ('Accepted', 'Accepted'),  ('Declined', 'Declined')), null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        organization = self.client_ID.organization.all().first()
        return f"{self.talent_ID.first_name.capitalize()} {self.talent_ID.last_name.capitalize()} ___{organization.name.capitalize()} --- Suggested"
