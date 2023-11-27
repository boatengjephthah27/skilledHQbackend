from rest_framework import viewsets, views, generics
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser, Organization, Address, Talent,  Degree, Project, TechnologiesUsed, Manager, SkillStack, Language, Social, Experience, Challenge, IdentityFiles
from .serializers import CustomUserSerializer, OrganizationSerializer, AddressSerializer, TalentSerializer,  DegreeSerializer,  ProjectSerializer, TechnologiesUsedSerializer, ManagerSerializer, LoginSerializer, SkillStackSerializer, LanguageSerializer, SocialSerializer, ExperienceSerializer, ChallengeSerializer, IdentityFilesSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from rest_framework.parsers import MultiPartParser, FormParser
from firebase_admin import auth
from django.http import JsonResponse
from django.conf import settings
from core.utils.api_errors import ApiError
from core.utils.api_responses import ApiResponse
import jwt
from core.utils.constants import COOKIE_NAME, ONE_DAY


# Create your views here.


class LoginView(views.APIView):
    permission_classes = [AllowAny,]

    def post(self, request):

        firebase_id_token = request.data.get('token')

        if firebase_id_token:
            decoded_token = auth.verify_id_token(firebase_id_token)
            user_email = decoded_token.get("email")
            name = user_email.split("@")[0]
            SECRET_KEY = settings.SECRET_KEY

            try:
                user = CustomUser.objects.get(email=user_email)
                serializer = CustomUserSerializer(user)

                payload = {
                    "user_id": str(user.id),
                    "email": user.email,
                    "is_client": user.is_client,
                    "iat": decoded_token.get("iat"),
                    "exp": decoded_token.get("exp"),
                }

                response = JsonResponse(serializer.data)
                jwt_token = jwt.encode(
                    payload, SECRET_KEY, algorithm="HS256")

                response.set_cookie(COOKIE_NAME, secure=True, value=str(
                    jwt_token), max_age=ONE_DAY, samesite='none', )

                return response

            except CustomUser.DoesNotExist:
                if user_email:
                    new_user = CustomUser(email=user_email, first_name=name)
                    new_user.save()
                    serializer = CustomUserSerializer(new_user)

                    response = JsonResponse(serializer.data)
                    jwt_token = jwt.encode(
                        payload, SECRET_KEY, algorithm="HS256").decode("utf-8")

                    response.set_cookie(COOKIE_NAME, secure=True, value=str(
                        jwt_token), max_age=ONE_DAY, samesite='none', )

                    return response

                else:
                    return JsonResponse({'error': 'Email is required for user creation'}, status=400)

        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)


class LogoutView(views.APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class SkillStackViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = SkillStack.objects.all()
    serializer_class = SkillStackSerializer


class IdentityFilesViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [AllowAny,]
    queryset = IdentityFiles.objects.all()
    serializer_class = IdentityFilesSerializer

    def post(self, request, format=None):
        serializer = IdentityFilesSerializer(data=request.data)

        if serializer.is_valid():
            # Save the file and other fields to the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class SocialViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Social.objects.all()
    serializer_class = SocialSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class TalentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Talent.objects.all()
    serializer_class = TalentSerializer


class TalentUserViewSet(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Talent.objects.all()
    serializer_class = TalentSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            user = Talent.objects.filter(user=user_id)
            return user

        return Talent.objects.none()


class DegreeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        try:
            user_id = request.data.get('user')
            talent_id = request.data.get('talent')
            if user_id != "":
                user_instance = CustomUser.objects.get(id=user_id)
                talent_instance = Talent.objects.get(id=talent_id)

                new_data = {
                    'position': request.data['position'],
                    'start_date': request.data['start_date'],
                    'end_date': request.data['end_date'],
                    'company': request.data['company'],
                    'description': request.data['description'],
                    'user': user_instance.id,
                    'talent': talent_instance.id,
                }
            else:
                new_data = {
                    'position': request.data['position'],
                    'start_date': request.data['start_date'],
                    'end_date': request.data['end_date'],
                    'company': request.data['company'],
                    'description': request.data['description'],
                    'user': "",
                    'talent': "",
                }
            serialized_data = self.get_serializer(data=new_data)
            serialized_data.is_valid(raise_exception=True)
            new_project = serialized_data.save()

            technologiesUsed = request.data.get("technologies")
            for tech in technologiesUsed:
                TechnologiesUsed.objects.create(
                    name=tech, project=new_project, user=user_instance)

            return Response("Data saved successfully", status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TechnologiesUsedViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = TechnologiesUsed.objects.all()
    serializer_class = TechnologiesUsedSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class GetManagerViewSet(generics.ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('client')
        if user_id:
            user = Manager.objects.filter(client=user_id)
            return user

        return Manager.objects.none()
