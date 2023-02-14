from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import CommonUser, Customer, Employee


class CommonUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = CommonUser
        fields = ("email", "slug", "password", "first_name", "last_name", "patronymic",)

        lookup_field = "slug"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug"
            }
        }


class CustomerSerializer(serializers.ModelSerializer):
    user= CommonUserSerializer()
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Customer
        fields = ('user', 'slug', 'telephone_number')

        lookup_field = "slug"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug"
            }
        }

    def create(self, validated_data) -> (Customer, CommonUser):
        """
        Overrode 'create' method specifically for the 'customer' field with nested serializer.
        """

        CommonUser_data = validated_data.pop('user')
        NewCommonUser = CommonUser(**CommonUser_data)
        NewCommonUser.set_password(CommonUser_data['password'])
        NewCommonUser.save()
        NewCustomer = Customer.objects.create(user=NewCommonUser, **validated_data)
        return NewCustomer

    def update(self, instance, validated_data):
        """
        Overrode 'update' method specifically for the 'customer' field with nested serializer.
        """
        # CommonUser_data = validated_data.pop('user')
        # UpdatedCommonUser = instance.user
        # UpdatedCommonUser.username = CommonUser_data.get('username', UpdatedCommonUser.username)
        # UpdatedCommonUser.email = CommonUser_data.get('email', UpdatedCommonUser.email)
        # UpdatedCommonUser.password = CommonUser_data.get('password', UpdatedCommonUser.password)
        # UpdatedCommonUser.first_name = CommonUser_data.get('first_name', UpdatedCommonUser.first_name)
        # UpdatedCommonUser.last_name = CommonUser_data.get('last_name', UpdatedCommonUser.last_name)
        # UpdatedCommonUser.patronymic = CommonUser_data.get('patronymic', UpdatedCommonUser.patronymic)
        # UpdatedCommonUser.save()
        #
        # instance.telephone_number = validated_data.get('telephone_number', instance.telephone_number)
        # instance.email = CommonUser_data.get('email', instance.email)
        # instance.save()
        #
        # return instance

        print('checked')

        user_data = validated_data.pop('user')
        user_serializer = CommonUserSerializer(instance=instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.update(instance.user, user_data)
        return super().update(instance, validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    user = CommonUserSerializer()

    class Meta:
        model = Employee

        fields = ('user', 'education', 'position')
