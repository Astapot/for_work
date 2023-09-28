from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from business.models import Product, UserForProduct, Lesson, UserLesson
from business.serializers import ProductSerializer, UserForProductSerializer, LessonSerializer
from django.http import HttpResponse
# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class UserForProductViewSet(ModelViewSet):
    queryset = UserForProduct.objects.all()
    serializer_class = UserForProductSerializer


def get_info_user(request, number):
    user = UserForProduct.objects.filter(id=number)
    product = Product.objects.filter(owner=number)
    string_products = 'продукты: '
    for i in product:
        string_products += str(i) + ','

    msg = str(user[0]) + string_products

    return HttpResponse(msg)


