from rest_framework import serializers
from .models import CustomUser, Organization, Address, Talent, Degree,  Project, TechnologiesUsed, Manager, SkillStack, Language, Social, Experience, Challenge, IdentityFiles
from django.contrib.auth import authenticate


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "city",
            "country",
            "location_link",
            "zip",
            'user'
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=True, read_only=True)
    organization = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'last_login',
            'email',
            'image',
            'gender',
            'first_name',
            'last_name',
            'age',
            'is_client',
            'contact',
            'date_created',
            'address',
            'organization'
        ]
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserSomeSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=True, read_only=True)
    organization = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'image',
            'first_name',
            'last_name',
            'contact',
            'address',
            'organization'
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'],
                            password=attrs['password'])
        if not user:
            raise serializers.ValidationError(
                'Incorrect email or password.')
        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')
        return {'user': user}


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'

        # [
        #     "id",
        #     "title",
        #     "start_date",
        #     "end_date",
        #     "country",
        #     "city",
        #     "institution",
        # ]


class TechnologiesUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnologiesUsed
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):

    technologies = TechnologiesUsedSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class SkillStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillStack
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = "__all__"


class IdentityFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityFiles
        fields = "__all__"


class TalentSerializer(serializers.ModelSerializer):
    degree = DegreeSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    skillStack = SkillStackSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    socials = SocialSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    challenge = ChallengeSerializer(many=True, read_only=True)
    identityCards = IdentityFilesSerializer(many=True, read_only=True)

    class Meta:
        model = Talent
        fields = [field.name for field in Talent._meta.fields] + \
            ['languages', 'socials', 'degree',
                'projects', 'skillStack', 'experience', 'challenge', 'identityCards', 'user', 'verified']


class CustomUserTalentSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=True, read_only=True)
    profile = TalentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'image',
            'first_name',
            'last_name',
            'gender',
            'contact',
            'address',
            'profile'
        ]
