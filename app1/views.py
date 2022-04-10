from rest_framework import viewsets
from app1 import serializers, models, controller, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        self.serializer_class = serializers.CreateAccountSerializer
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk=None):
        if not request.user.id:
            return Response(data="you need a token for this endpoint", status=401)
        if request.user.id != int(pk):
            return Response(data="you can only get the info for your account", status=401)
        return super().retrieve(request, pk)

    def update(self, request, pk=None):
        self.serializer_class = serializers.UpdateAccountSerializer
        if not request.user.id:
            return Response(data="you need a token for this endpoint", status=401)
        if request.user.id != int(pk):
            return Response(data="you can only update your account", status=401)
        return super().update(request, pk)

    def partial_update(self, request, pk=None):
        self.serializer_class = serializers.UpdateAccountSerializer
        if not request.user.id:
            return Response(data="you need a token for this endpoint", status=401)
        if request.user.id != int(pk):
            return Response(data="you can only update your account", status=401)
        return super().partial_update(request, pk)

    def destroy(self, request, pk=None):
        if not request.user.id:
            return Response(data="you need a token for this endpoint", status=401)
        if request.user.id != int(pk):
            return Response(data="you can only delete your account", status=401)
        # self.serializer_class.delete(pk=pk)
        return super().destroy(request, pk)

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            account = models.Account.objects.get(user__id=request.user.id)
        except:
            return Response(status=404)
        return Response(data=serializers.AccountSerializer(account).data, status=200)

    @action(detail=False, methods=['put'])
    def redeem_daily_tickets(self, request):
        if not request.user.id:
            return Response(data="you need a token for this endpoint", status=401)
        try:
            user = controller.redeem_free_daily_tickets(request.user)
            response = serializers.AccountSerializer(user.account).data
            response = {
                'message': "Daily free tickets redeem.",
                'account': response
            }
            return Response(data=response, status=200)
        except exceptions.AlreadyRedeemDailyCode as e:
            return Response(data=e.message, status=400)


class MathViewSet(viewsets.ModelViewSet):
    queryset = models.Math.objects.all()
    serializer_class = serializers.MathSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'put']

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request)
        except exceptions.NotEnoughTicketsException as e:
            return Response(
                data={
                    'message': e.message,
                    'points_needed': e.points_needed,
                    'points_available': e.points_available
                },
                status=400
            )

    @action(detail=True, methods=['put'])
    def draw_card(self, request, pk):
        try:
            math = models.Math.objects.get(pk=pk)
            controller.user_is_authorized(request.user, math)
            controller.draw_player_card(math)
            response = serializers.MathSerializer(math)
            return Response(data=response.data, status=200)
        except models.Math.DoesNotExist:
            return Response(status=404)
        except exceptions.IsOutException as e:
            response = {
                'message': e.message,
                'math': serializers.MathSerializer(math).data
            }
            return Response(data=response, status=400)
        except exceptions.UnauthorizedPlayerException as e:
            return Response(data=e.message, status=401)

    @action(detail=True, methods=['put'])
    def hold(self, request, pk):
        try:
            math = models.Math.objects.get(pk=pk)
            controller.user_is_authorized(request.user, math)
            is_player_win, math = controller.hold_round(math)
            if is_player_win:
                message = 'Congratulations, you won this round!'
            else:
                message = 'Sorry, you lose this round.'
            response = {
                'message': message,
                'math': serializers.MathSerializer(math).data
            }
            return Response(data=response, status=200)
        except models.Math.DoesNotExist:
            return Response(status=404)
        except exceptions.AlreadyHoldException as e:
            resp = {
                'message': e.message,
                'math': serializers.MathSerializer(math).data
            }
            return Response(data=resp, status=200)
        except exceptions.UnauthorizedPlayerException as e:
            return Response(data=e.message, status=401)

    @action(detail=True, methods=['put'])
    def next_round(self, request, pk):
        try:
            math = models.Math.objects.get(pk=pk)
            controller.user_is_authorized(request.user, math)
            math = controller.next_round(math)
            return Response(data=serializers.MathSerializer(math).data, status=200)
        except models.Math.DoesNotExist:
            return Response(status=404)
        except exceptions.MathIsOverException as e:
            resp = {
                'math_is_over': True,
                'message': e.message,
                'math': serializers.MathSerializer(math).data
            }
            return Response(data=resp, status=200)
        except exceptions.UnauthorizedPlayerException as e:
            return Response(data=e.message, status=401)
