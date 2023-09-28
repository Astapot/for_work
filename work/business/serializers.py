from rest_framework import serializers
from .models import UserForProduct, Product, Lesson, UserLesson, UserProduct, ProductLesson


class ProductLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLesson
        fields = ['id', 'product']

class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProduct
        fields = ['id', 'user']



class UserForProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserForProduct
        fields = ['id', 'login', 'productspos', 'views']
        read_only_fields = ['productspos', 'views']


class UserLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLesson
        fields = ['id', 'user', 'viewed_time', 'status']


class LessonSerializer(serializers.ModelSerializer):
    prods = ProductLessonSerializer(many=True)
    users = UserLessonSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'duration', 'users', 'prods']

    def create(self, validated_data):
        print(validated_data)
        users = validated_data.pop('users')
        prods = validated_data.pop('prods')
        lesson = super().create(validated_data)
        for i in users:
            i['lesson'] = lesson
            if i['viewed_time'] >= 0.8 * validated_data['duration']:
                i['status'] = 'Viewed'
            UserLesson.objects.update_or_create(
                **i
            )
        for i in prods:
            i['lesson'] = lesson
            ProductLesson.objects.update_or_create(
                **i
            )
        return lesson


class ProductSerializer(serializers.ModelSerializer):
    userown = UserProductSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'owner', 'product', 'userown']

    def create(self, validated_data):
        print(validated_data)
        userown = validated_data.pop('userown')
        product = super().create(validated_data)
        for i in userown:
            i['product'] = product
            # print(i)
            UserProduct.objects.update_or_create(
                **i
            )
        return product





