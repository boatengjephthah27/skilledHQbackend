from django.db import models
from django.forms import model_to_dict
# from core.utils.base import ApiBaseModel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
from core.utils.constants import SERVICE, SKILL_STACK, LANGUAGES, SOCIAL_MEDIA, FILE_TYPES

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        :param email: The email address of the user.
        :param password: The password for the user. If not provided, a random password will be generated.
        :param extra_fields: Any additional fields to set on the user model.
        :return: The newly created user.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        return self.create_user(email, password, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    image = models.FileField(upload_to="users_profile/", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(
        ('Male', 'Male'), ('Female', 'Female')), null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    age = models.IntegerField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)
    contact = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}  -  {self.email} "

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    image = models.FileField(
        upload_to="organization_profile/", null=True, blank=True)
    contact = models.CharField(max_length=100)
    client_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='organization')

    def __str__(self):
        return self.name.upper()


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    location_link = models.CharField(max_length=500, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return f" {self.user.first_name.capitalize()} {self.user.last_name.capitalize()} -  {self.country.capitalize()}, {self.city.capitalize()} ({self.street.capitalize()})"


class Talent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.CharField(
        max_length=25, choices=SERVICE, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    rate_per_hour = models.IntegerField(null=True, blank=True)
    full_time = models.BooleanField(null=True, blank=True, default=True)
    full_time_hours = models.IntegerField(null=True, blank=True)
    part_time = models.BooleanField(null=True, blank=True, default=True)
    part_time_hours = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    years_experience = models.IntegerField(null=True, blank=True)
    membership_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    remote = models.CharField(max_length=5, choices=(
        ('Yes', 'Yes'), ('No', 'No')), null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='profile')

    # def __str__(self):
    #     return f"{self.user.first_name.capitalize()} {self.user.last_name.capitalize()} - {self.role.capitalize()} "


class Degree(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    talent = models.ForeignKey(
        Talent, on_delete=models.CASCADE, null=True, blank=True, related_name='degree')

    def __str__(self):
        return f"{self.user.first_name.capitalize()} {self.user.last_name.capitalize()} - {self.title.capitalize()}, {self.institution.upper()} "


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    talent = models.ForeignKey(
        Talent, on_delete=models.CASCADE, null=True, blank=True, related_name='projects')

    def __str__(self):
        return f"{self.user.first_name.capitalize()} {self.user.last_name.capitalize()} - {self.position.capitalize()}, ({self.company.upper()}) "


class TechnologiesUsed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='technologies')
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name.capitalize()} {self.user.last_name.capitalize()} ({self.project.position.capitalize()})  -  , ({self.project.company.upper()}) -  [ {self.name.capitalize()} ] "


class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.CharField(max_length=25, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    slack = models.CharField(max_length=255, null=True, blank=True)
    whatsapp = models.CharField(max_length=255, null=True, blank=True)
    client = models.ManyToManyField(
        CustomUser, related_name='clients', blank=True)

    def __str__(self):
        return f"{self.full_name.capitalize()} - {self.email.capitalize()}"


class SkillStack(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(
        max_length=100, choices=SKILL_STACK, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    talent = models.ForeignKey(
        Talent, on_delete=models.CASCADE, null=True, blank=True, related_name='skillStack')
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name.capitalize()}  -  {self.talent.role.capitalize()} - ({self.type.capitalize()}, {self.name.capitalize()}) "


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(
        choices=LANGUAGES, max_length=30, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    talent = models.ForeignKey(
        Talent, on_delete=models.CASCADE, null=True, blank=True, related_name='languages')

    def __str__(self):
        return f"{self.user.first_name.capitalize()}  {self.user.last_name.capitalize()}  -  {self.language.capitalize()}"


class Social(models.Model):
    id = models.AutoField(primary_key=True)
    social_media = models.CharField(
        choices=SOCIAL_MEDIA, max_length=30, null=True, blank=True)
    media_link = models.CharField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    talent = models.ForeignKey(
        Talent, on_delete=models.CASCADE, null=True, blank=True, related_name='socials')

    def __str__(self):
        return f"{self.user.first_name.capitalize()}  {self.user.last_name.capitalize()}  -  ({self.social_media.capitalize()})"


class Experience(models.Model):
    id = models.AutoField(primary_key=True)
    tool = models.CharField(max_length=255, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    talent = models.ForeignKey(
        Talent, on_delete=models.CASCADE, null=True, blank=True, related_name='experience')

    def __str__(self):
        return f"{self.user.first_name.capitalize()}  {self.user.last_name.capitalize()}  -  ({self.tool.capitalize()} - {self.years}  )"


class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    challenge = models.CharField(max_length=500, null=True, blank=True)
    solution = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    talent = models.ForeignKey(
        Talent, on_delete=models.CASCADE, null=True, blank=True, related_name='challenge')

    def __str__(self):
        return f"{self.user.first_name.capitalize()}  {self.user.last_name.capitalize()}"


class IdentityFiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        choices=FILE_TYPES, max_length=25, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(
        upload_to="users_fileUploads/", null=True, blank=True)
    talent = models.ForeignKey(
        Talent, on_delete=models.CASCADE, null=True, blank=True, related_name='identityCards')

    def __str__(self):
        return f"{self.title.capitalize()} - {self.type.capitalize()}"


# const requestPromises = dataToPatch.map(({ data, endpoint }) => {
# 			return axios.put(endpoint, data);
# 		});

# 		const postrequestPromises = dataToPost.map(({ data, endpoint }) => {
# 			return axios.post(endpoint, data);
# 		});

# 		if (!profile?.id && user?.address[0]?.length < 1) {
# 			Promise.all(postrequestPromises)
# 				.then((responses) => {
# 					SetToast({
# 						view: true,
# 						message: "Personal Info Updated!",
# 						type: "success",
# 					});

# 					setTimeout(() => {
# 						getTalent();
# 						getUser();
# 					}, 300);

# 					responses.forEach((response, index) => {
# 						console.log(`Response for request ${index + 1}:`, response.data);
# 					});
# 				})
# 				.catch((error) => {
# 					console.error("Error:", error);
# 					SetToast({
# 						view: true,
# 						message: "Update Unsuccessful!",
# 						type: "error",
# 					});
# 				});
# 		} else {
# 			Promise.all(requestPromises)
# 				.then((responses) => {
# 					SetToast({
# 						view: true,
# 						message: "Personal Info Updated!",
# 						type: "success",
# 					});

# 					setTimeout(() => {
# 						getTalent();
# 						getUser();
# 					}, 300);

# 					responses.forEach((response, index) => {
# 						console.log(`Response for request ${index + 1}:`, response.data);
# 					});
# 				})
# 				.catch((error) => {
# 					console.error("Error:", error);
# 					SetToast({
# 						view: true,
# 						message: "Update Unsuccessful!",
# 						type: "error",
# 					});
# 				});
# 		}
