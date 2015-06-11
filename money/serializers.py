from rest_framework import serializers
from money.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'last_login',
            'date_joined',
        )


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = (
            'url',
            'title',
            'created_at',
        )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = (
            'url',
            'title',
            'affected_limit',
            'created_at',
        )


class TransferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transfer
        fields = (
            'url',
            'account_from',
            'account_to',
            'user',
            'amount',
            'comment',
            'created_at',
        )


class OperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operation
        fields = (
            'url',
            'account',
            'category',
            'transfer',
            'user',
            'amount',
            'type',
            'comment',
            'created_at',
        )


class GoalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goal
        fields = (
            'url',
            'title',
            'amount',
            'percent',
            'account',
            'created_at',
        )
