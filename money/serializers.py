from django.contrib.auth.models import User, Group
from rest_framework import serializers
from money.models import *


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username']


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'title', 'balance']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category


class TransferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transfer


class OperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operation


class GoalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goal
        fields = ['url', 'title', 'amount']
