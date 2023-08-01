import json

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#------------------------------------------------------------------
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, error_messages={
        'blank': ' password_field_cannot_be_blank.',

    })
    username = serializers.CharField(error_messages={ 'blank': 'username field cannot be blank.',}
                                     ,validators=[UniqueValidator(queryset=User.objects.all(),message='Username_already_taken.')])

    email = serializers.EmailField(error_messages={'blank':'email field cannot be blank',}
                                   ,validators=[UniqueValidator(queryset=User.objects.all(),message='email_already_taken.')])
    # username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(),message='Username already exists.')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



    def create(self, validated_data):

        user = User.objects.create(
                    username=validated_data['username'],
                    email=validated_data['email']
                )
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def validate(self, attrs):
    #     # Perform additional custom validation checks here
    #     # You can access the validated data through the 'attrs' dictionary
    #     # If validation fails, raise a 'serializers.ValidationError' with an appropriate error message
    #
    #     # Example: Check if username is already taken
    #     username = attrs.get('username')
    #     if User.objects.filter(username=username).exists():
    #         raise serializers.ValidationError('Username_is_already_taken.')
    #
    #     return attrs

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, error_messages={
#         'required': 'Custom error message for password field.',
#     })
#     username = serializers.CharField(error_messages={
#         'required': 'Custom error message for username field.',
#     })
#     email = serializers.EmailField(error_messages={
#         'required':'email required',
#         'invalid': 'invalid email.',
#     })
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')


    # def validate_email(self, value):
    #     if value == '':
    #         raise serializers.ValidationError('Custom error message for required email field.')
    #     return value
    # def validate(self, data):
    #     print("vali********")
    #     username = data.get('username')
    #     print(username)
    #     password = data.get('password')
    #     print(password)
    #     email = data.get('email')
    #     print(email)
    #     print(data["username"])
    #     print(data["password"])
    #     print(data["email"])
        # data["password"]='s'
        # print("dp",data["password"])


        # if  data["email"]==None:
        #     # pass
        #
        #     raise serializers.ValidationError('Please enter a valid email .')
        # if 'username' in data and  ErrorDetail(string=='This field may not be blank.'):
        #     raise serializers.ValidationError('Please enter a valid username .')


        # if data["password"]==None:
        #     raise serializers.ValidationError('Please enter a valid password .')

        # if email=="":
        #     raise serializers.ValidationError('Please enter a valid email .')



        # return data



class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(error_messages={
        'blank': ' password_field_cannot_be_blank.'
    })

    username = serializers.CharField(error_messages={
        'blank': 'username_field_cannot_be_blank.'
    })



    class Meta:
            model = User
            fields = ('username', 'password')


# raise serializers.ValidationError("username no way")

# raise serializers.ValidationError("password no way")




class usermachineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Machines_List
        fields = "__all__"



class generalmachineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Machines_List
        fields = ('machine_id', 'machine_name', 'machine_location', 'date_of_installation')


class IostatusmachineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Machines_List
        fields = ('id', 'machine_name', 'digital_input','digital_output','analog_input','analog_output')

class Machines_List_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Machines_List
        fields = ('machine_name','machine_location',)


class kpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine_Kpi_List
        fields = "__all__"

class plantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant_List
        fields="__all__"

class plantSerializerr(serializers.ModelSerializer):
    class Meta:
        model = Plant_List
        fields=('plant_name',)



class modelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_List
        fields="__all__"





class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_List
        fields=('company_name',)



class lineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line_List
        fields="__all__"



# class DropdownSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = '__all__'
#
#

class all_Machine_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model=all_Machine_data
        fields = ('plant_name','model_name','line_name')



class all_Machine_data_Serializer2(serializers.ModelSerializer):
    class Meta:
        model=all_Machine_data
        # fields = '__all__'
        fields = ('company_name','plant_name','machine_id','model_name','line_name')










class ReportEntrySerializer(serializers.Serializer):
    machine_id = serializers.CharField(max_length=10)
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    report_type = serializers.CharField(max_length=50)