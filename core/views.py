from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Product
from core.serializers import ProductSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@ensure_csrf_cookie
def Index(request):
    return render(request,template_name = 'valavala.html')


@login_required
def Dashboard(request):
    return render(request, template_name = 'dashboard.html')

class LoginView(APIView):
    
    def post(self,request,*args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username,
                                password=password
                                )
            if user is None:
                return Response({
                    'detail':'Invalid username or passoword',
                    'success':False
                },status=status.HTTP_400_BAD_REQUEST)
            
            login(request, user)
            return Response({
                'detail':'Login Successful...',
                'success':True,
                'url': 'api/dashboard/' 
            },status=status.HTTP_200_OK)
        
        except Exception as exp:
            return Response({
                'detail':str(exp),
                'success':False
            },status=status.HTTP_400_BAD_REQUEST)


class ProductHandler(APIView):
    parser_classes = [MultiPartParser, FormParser]


    def get(self,request,*args, **kwargs):
        try:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset,many=True)
            return Response({
                'data':serializer.data,
                'success':True
            },status=status.HTTP_200_OK)
        
        except Exception as exp:
            return Response({
                'detail':str(exp),
                'success':False
            },status=status.HTTP_200_OK)
    
    def post(self,request,*args, **kwargs):
        try:
            print(request.data)
            serializer = ProductSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success':True,
                    'data':serializer.data
                },status=status.HTTP_201_CREATED) 
            print(serializer.errors)
            return Response({
                'detail':'Form has some errors',
                'success':False
            },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as exp:
            return Response({
                'detail':str(exp),
                'success':False
            },status=status.HTTP_400_BAD_REQUEST)

class DasbboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        try:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset,many=True)
            return Response({
                'data':serializer.data,
                'success':True
            },status=status.HTTP_200_OK)
        
        except Exception as exp:
            return Response({
                'detail':str(exp),
                'success':False
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateProduct(APIView):
    def patch(self,request,prod_id,*args, **kwargs):
        try:
            print(request.data)
            product = Product.objects.get(id=prod_id)
            if not product:
                return Response({
                    'detail':'Product was not found. Perhaps it was deleted'
                })
            product.name = request.data.get("name")
            product.badge = request.data.get('badge')
            product.category = request.data.get('category')
            product.desc = request.data.get('desc')

            product.save()
            serializer = ProductSerializer(product)
            return Response({
                'product':serializer.data,
                'success':True
            },status=status.HTTP_200_OK)
        
        except Exception as exp:
            print(exp)
            return Response({
                'detail':str(exp),
                'success':False,
            },status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,*args, **kwargs):
        pass