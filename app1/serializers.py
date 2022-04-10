import datetime

from rest_framework import serializers
from app1 import models, exceptions, controller
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active']


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Account
        fields = ['id', 'user', 'tickets']

    # def delete(self, pk):
    #     print('foi')
    #     instance = models.Account.objects.get(pk=pk)
    #     instance.user.delete


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreateAccountSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()

    class Meta:
        model = models.Account
        fields = ['user', 'tickets']

    def create(self, validated_data):
        user = validated_data.get('user')
        user = User.objects.create_user(username=user.get('username'), email=user.get('email'), password=user['password'])
        return models.Account.objects.create(user=user, tickets=validated_data.get('tickets'))


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UpdateAccountSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()

    class Meta:
        model = models.Account
        fields = ['user', 'tickets']

    def update(self, instance, validated_data):
        user = validated_data['user']
        instance.user.first_name = user['first_name']
        instance.user.last_name = user['last_name']
        instance.user.email = user['email']
        instance.tickets = validated_data['tickets']
        instance.user.save()
        instance.save()
        return instance


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = '__all__'


class HandSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = models.Hand
        fields = '__all__'


class MathSerializer(serializers.ModelSerializer):
    buy_in_value = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Math
        fields = '__all__'
        read_only_fields = ['prize', 'date', 'active_round', 'is_win', 'rounds_won']

    def create(self, validated_data):
        account = models.Account.objects.get(pk=validated_data['account'].id)
        if account.tickets >= validated_data['buy_in_value']:
            account.tickets -= int(validated_data['buy_in_value'])
            account.save()
            math = models.Math.objects.create(
                prize=int(validated_data['buy_in_value']) * 2,
                date=datetime.datetime.now(),
                active_round=1,
                account=account,
                is_win=False,
                rounds_won=0
            )
            player_hand = models.Hand.objects.create(
                round=math.active_round,
                math=math,
                total_point=0,
                is_out=False,
                is_player_hand=True
            )
            dealer_hand = models.Hand.objects.create(
                round=math.active_round,
                math=math,
                total_point=0,
                is_out=False,
                is_player_hand=False
            )
            for number in [1, 2]:
                controller.create_card(player_hand, number)
            for number in [1, 2]:
                controller.create_card(dealer_hand, number)

            controller.get_points(math)
            return math
        else:
            raise exceptions.NotEnoughTicketsException(available=account.tickets, needed=validated_data['buy_in_value'])

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        player_hand = models.Hand.objects.get(math=instance, round=instance.active_round, is_player_hand=True)
        dealer_hand = models.Hand.objects.get(math=instance, round=instance.active_round, is_player_hand=False)
        ret['player_hand'] = HandSerializer(player_hand).data
        if player_hand.is_hold:
            ret['dealer_hand'] = HandSerializer(models.Hand.objects.get(math=instance, round=instance.active_round,
                                                                        is_player_hand=False)).data
        else:
            ret['dealer_hand'] = [
                {
                    'value': '?',
                    'img_url': '?',
                    'position': '0'
                },
                CardSerializer(dealer_hand.cards.all()[1]).data
            ]
        return ret

