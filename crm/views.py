from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponse
from rest_framework import generics, viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from .models import CustomAnswer, CustomQuestion, Contact, Event, UserProfile, Group, UserProfileField
from .serialisers import ContactSerializer, UserProfileSerializer, UserAccountSerializer, PermissionSerializer, GroupSerializer, UserProfileFieldSerializer, CustomQuestionSerializer, CustomAnswerSerializer # , CustomContactSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the index.")


"""
Home page user gets redirected to after login. Currently only displays information about the current user
"""
class HomeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = self.request.user.userprofile
        serializer = UserProfileSerializer(user,  context={'request': request})
        return Response(serializer.data)


# class CustomContact:
#     def __init__(self, contact):
#         self.contact = contact
#         self.answers = CustomAnswer.objects.filter(contact=contact)
        
#     def create(self, validated_data):
#         return CustomContact(**validated_data)
    
#     def __str__(self):
#         return str(self.contact) + "   " + str(self.answers)

# class CustomContactViewSet(viewsets.ViewSet):
#     contacts = Contact.objects.all()
#     queryset = [CustomContact(contact) for contact in contacts]
#     serializer_class = CustomContactSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def list(self, request):
#         user = self.request.user.userprofile
#         contacts = Contact.objects.filter(contactOwner=user)
#         customContacts = [CustomContact(contact) for contact in contacts]
#         serializer = CustomContactSerializer(customContacts, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def create(self, request):
#         pass
        
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('whenAdded')
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    """
    Only shows contacts that the user owns.
    """
    def list(self, request):
        user = self.request.user.userprofile
        queryset = Contact.objects.filter(contactOwner=user)
        serializer = ContactSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    """
    Displays all contacts in the database.
    """
    # NOTE: For testing purposes only. Should add a permission modifier for only admins to access
    @action(detail=False)
    def all_contacts(self, request):
        queryset = Contact.objects.all()
        serializer = ContactSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    # NOTE: Not sure how this works lol
    # def retrieve(self, request, pk=None):
    #     query = Contact.objects.get(pk=pk)
    #     serializer = ContactSerializer(query, context={'request': request})
    #     return Response(serializer.data)
    
    """
    Gets all the custom answers for a specific contact.
    """
    @action(detail=True)
    def get_answer(self, request, pk=None):
        contact = Contact.objects.get(pk=pk)
        
        filled_questions = {answer.question for answer in CustomAnswer.objects.filter(contact = contact)}
        blank_questions = CustomQuestion.objects.filter(user = request.user.userprofile)
        for q in blank_questions:
            if q not in filled_questions:
                CustomAnswer.objects.create(question = q, contact=contact, data = "")
        
        # returns all answers
        queryset = CustomAnswer.objects.filter(contact = contact)
        serializer = CustomAnswerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    """
    Creates a new contact, owned by the current user.
    """
    def perform_create(self, serializer):
        serializer.save(contactOwner=self.request.user.userprofile)

    # NOTE: Overwritten these functions currently, investigate what needs to be edited for our purposes
    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass


# TODO: Make the following edpoints dynamic based on which user has logged in


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Allows access to all user profiles in the database.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]



"""
API Endpoint to verify if a user email already exists.
"""
@csrf_exempt  # temporarily disable csrf token
@api_view(['POST'])
def check_email(request):
    queryset = User.objects.values_list('username', flat=True)
    body = json.loads(request.body)
    exists = body['email'] in queryset
    response = JsonResponse({'success': exists})
    response["Access-Control-Allow-Origin"] = "*"
    return response

"""
Login user.
"""
@csrf_exempt  # temporarily disable csrf token
@api_view(['POST'])
def login(request):
    body = json.loads(request.body)
    user = authenticate(username=body['username'], password=body['password'])
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'success': True, 'id': user.id, 'username': user.username, 'token': token.key })
    else:
        return JsonResponse({'success': False})

"""
User Profile custom fields
"""
@csrf_exempt  # temporarily disable csrf token
@api_view(['GET', 'POST'])
def get_profile_fields(request, id):
    if request.method == 'GET':
        fields = UserProfileField.objects.filter(userAccount=id)
        serializer = UserProfileFieldSerializer(fields, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        UserProfileField.objects.filter(userAccount=id).delete()
        serializer = UserProfileFieldSerializer(data=request.data['fields'], many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountViewSet(viewsets.ModelViewSet):
    """
    Allows access to all user accounts in the database.
    """
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    #permission_classes = [permissions.IsAuthenticated]


class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows permissions to be viewed or edited.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        user = self.request.user.userprofile
        queryset = Group.objects.filter(groupOwner=user)
        serializer = GroupSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    # NOTE: For testing purposes only. Should add a permission modifier for only admins to access
    @action(detail=False)
    def all_groups(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add_contact/(?P<contact_pk>[^/.]+)')
    def add_contact(self, request, contact_pk, pk):
        group = self.get_object()
        contact = Contact.objects.get(id=contact_pk)
        if contact.contactOwner == self.request.user.userprofile:
            group.contacts.add(contact)
            group.save()
        return Response()  # TODO: fix redirect
    
    def perform_create(self, serializer):
        serializer.save(groupOwner=self.request.user.userprofile)




class CustomQuestionViewSet(viewsets.ModelViewSet):
    queryset = CustomQuestion.objects.all()
    serializer_class = CustomQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        user = self.request.user.userprofile
        queryset = CustomQuestion.objects.filter(user = user)
        serializer = CustomQuestionSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user.userprofile)
        
        
class CustomAnswerViewSet(viewsets.ModelViewSet):
    queryset = CustomAnswer.objects.all()
    serializer_class = CustomAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
