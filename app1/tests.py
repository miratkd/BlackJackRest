import datetime
from rest_framework.test import APITestCase
from oauth2_provider.models import get_access_token_model, get_application_model
from django.contrib.auth import get_user_model
from app1 import models, controller
import json


Application = get_application_model()
AccessToken = get_access_token_model()
UserModel = get_user_model()


class SystemTest(APITestCase):

    def setUp(self):
        self.test_user = UserModel.objects.create_user("test_user", "test@user.com", "123456")
        self.account = models.Account.objects.create(user=self.test_user, tickets=100000)

        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type="password",
        )
        self.application.save()

    def test_login(self):
        response = self.login('test_user', '123456')
        token = json.loads(response.content.decode('utf-8')).get('access_token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(token is not None, True)

    def login(self, user, password):
        data = {
            'grant_type': 'password',
            'username': user,
            'password': password,
            'client_id': self.application.client_id,
            'client_secret': self.application.client_secret
        }
        return self.client.post('/o/token/', data)

    def test_create_account(self):
        name = 'create-user'
        email = "lucasmira2011@gmail.com"
        password = "13972684"
        data = {
            'user': {
                'username': name,
                "email": email,
                "password": password
            },
            "tickets": "100"
        }
        response = self.client.post('/account/', data, format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content.get('user') is not None, True)
        self.assertEqual(content.get('user').get('username'), name)
        self.assertEqual(content.get('user').get('email'), email)
        response = self.login(name, password)
        token = json.loads(response.content.decode('utf-8')).get('access_token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(token is not None, True)

    def test_daily_free_tickets(self):
        response = self.login('test_user', '123456')
        token = json.loads(response.content.decode('utf-8')).get('access_token')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/account/me/')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        tickets = content.get('tickets')
        response = self.client.put('/account/redeem_daily_tickets/')
        content = json.loads(response.content.decode('utf-8'))
        new_tickets = content.get('account').get('tickets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.get('message'), 'Daily free tickets redeem.')
        self.assertEqual(new_tickets, tickets + 200)
        response = self.client.put('/account/redeem_daily_tickets/')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, 'have you redeemed your daily tickets today.')
        response = self.client.get('/account/me/')
        content = json.loads(response.content.decode('utf-8'))
        tickets = content.get('tickets')
        self.assertEqual(tickets, new_tickets)

    def test_math(self):
        self.math()
        self.math()
        self.math()
        self.math()
        self.math()
        self.math()

    def math(self):
        response = self.login('test_user', '123456')
        token = json.loads(response.content.decode('utf-8')).get('access_token')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.account.tickets = 50
        self.account.save()
        buy_in = 100
        data = {"account": self.account.id,
                "buy_in_value": buy_in}
        response = self.client.post('/math/', data, format='json')
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content.get('message'), 'You doest have enough tickets for this actions')
        self.assertEqual(content.get('points_needed'), buy_in)
        self.assertEqual(content.get('points_available'), self.account.tickets)
        self.account.tickets = 100
        self.account.save()
        data = {"account": self.account.id,
                "buy_in_value": buy_in}
        response = self.client.post('/math/', data, format='json')
        content = json.loads(response.content.decode('utf-8'))
        self.math_id = content.get('id')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content.get('prize'), buy_in * 2)
        self.assertEqual(content.get('math_active_round'), 1)
        self.math_active_round = content.get('math_active_round')
        self.assertEqual(content.get('is_win'), False)
        self.assertEqual(content.get('rounds_won'), 0)
        self.rounds_won = content.get('rounds_won')
        self.assertEqual(content.get('is_over'), False)
        self.assertEqual(content.get('account'), self.account.id)
        self.chose_action(content)

    def chose_action(self, content):
        self.assertEqual(content.get('math_active_round'), content.get('player_hand').get('round'))
        if content.get('player_hand').get('total_point') < 22:
            self.assertEqual(content.get('player_hand').get('is_out'), False)
            if content.get('player_hand').get('total_point') < 16:
                self.draw_a_card()
            else:
                self.hold()
        else:
            self.assertEqual(content.get('player_hand').get('is_out'), True)
            self.next_round()

    def draw_a_card(self):
        response = self.client.put('/math/'+str(self.math_id)+'/draw_card/')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.chose_action(content)
        # self.assertEqual(content.get('math_active_round'), content.get('player_hand').get('round'))
        # self.assertEqual(content.get('math_active_round'), content.get('dealer_hand').get('round'))
        # if content.get('total_point') < 22:
        #     self.assertEqual(content.get('is_out'), False)
        #     if content.get('total_point') < 16:
        #         self.draw_a_card()
        #     else:
        #         self.hold()
        # else:
        #     self.assertEqual(content.get('is_out'), True)

    def hold(self):
        response = self.client.put('/math/' + str(self.math_id) + '/hold/')
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.get('math').get('math_active_round'), content.get('math').get('player_hand').get('round'))
        self.assertEqual(content.get('math').get('math_active_round'), content.get('math').get('dealer_hand').get('round'))
        player_points = content.get('math').get('player_hand').get('total_point')
        dealer_points = content.get('math').get('dealer_hand').get('total_point')
        if dealer_points < player_points < 22 or dealer_points > 21:
            self.assertEqual(content.get('message'), 'Congratulations, you won this round!')
            self.assertEqual(content.get('math').get('rounds_won'), self.rounds_won + 1)
            self.rounds_won += 1
            # if content.get('math').get('rounds_won') > 4:
            #     self.assertEqual(content.get('math').get('is_win'), True)
            #     self.assertEqual(content.get('math').get('is_over'), True)
            #     # continue...
            # else:
            self.next_round()
        else:
            self.assertEqual(content.get('message'), 'Sorry, you lose this round.')
            self.assertEqual(content.get('math').get('rounds_won'), self.rounds_won)
            dealer_wins = (content.get('math').get('math_active_round') - 1) - content.get('math').get('rounds_won')
            # if dealer_wins > 4:
            #     self.assertEqual(content.get('math').get('is_win'), False)
            #     self.assertEqual(content.get('math').get('is_over'), True)
            #     # continue...
            # else:
            self.next_round()

    def next_round(self):
        response = self.client.put('/math/' + str(self.math_id) + '/next_round/')
        content = json.loads(response.content.decode('utf-8'))

        if content.get('math_is_over'):
            if content.get('math').get('rounds_won') > 4:
                self.assertEqual(content.get('math').get('is_win'), True)
                self.assertEqual(content.get('math').get('is_over'), True)
                response = self.client.get('/account/me/')
                content = json.loads(response.content.decode('utf-8'))
                self.assertEqual(content.get('tickets'), 200)
            else:
                self.assertEqual(content.get('math').get('is_win'), False)
                self.assertEqual(content.get('math').get('is_over'), True)

            return
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.get('math_active_round'), self.math_active_round + 1)
        self.math_active_round += 1
        self.chose_action(content)

    def test_points_1(self):
        math = models.Math.objects.create(
            prize=500,
            date=datetime.datetime.now(),
            math_active_round=1,
            account=self.account,
            rounds_won=0,
        )
        player_hand = models.Hand.objects.create(
            round=1,
            math=math,
            total_point=0,
            is_out=False,
            is_player_hand=True,
            is_hold=False
        )
        models.Card.objects.create(
            hand=player_hand,
            value=1,
            img_url='?',
            position=0
        )
        models.Card.objects.create(
            hand=player_hand,
            value=10,
            img_url='?',
            position=1
        )
        dealer_hand = models.Hand.objects.create(
            round=1,
            math=math,
            total_point=0,
            is_out=False,
            is_player_hand=False,
            is_hold=False
        )
        models.Card.objects.create(
            hand=dealer_hand,
            value=10,
            img_url='?',
            position=0
        )
        models.Card.objects.create(
            hand=dealer_hand,
            value=8,
            img_url='?',
            position=1
        )
        controller.get_points(math)
        player_hand = models.Hand.objects.get(pk=player_hand.id)
        dealer_hand = models.Hand.objects.get(pk=dealer_hand.id)
        self.assertEqual(player_hand.total_point, 21)
        self.assertEqual(player_hand.is_out, False)
        self.assertEqual(dealer_hand.total_point, 18)
        self.assertEqual(dealer_hand.is_out, False)

    def test_points_2(self):
        math = models.Math.objects.create(
            prize=500,
            date=datetime.datetime.now(),
            math_active_round=1,
            account=self.account,
            rounds_won=0,
        )
        player_hand = models.Hand.objects.create(
            round=1,
            math=math,
            total_point=0,
            is_out=False,
            is_player_hand=True,
            is_hold=False
        )
        models.Card.objects.create(
            hand=player_hand,
            value=1,
            img_url='?',
            position=0
        )
        models.Card.objects.create(
            hand=player_hand,
            value=1,
            img_url='?',
            position=1
        )
        models.Card.objects.create(
            hand=player_hand,
            value=5,
            img_url='?',
            position=2
        )
        dealer_hand = models.Hand.objects.create(
            round=1,
            math=math,
            total_point=0,
            is_out=False,
            is_player_hand=False,
            is_hold=False
        )
        models.Card.objects.create(
            hand=dealer_hand,
            value=10,
            img_url='?',
            position=0
        )
        models.Card.objects.create(
            hand=dealer_hand,
            value=10,
            img_url='?',
            position=1
        )
        models.Card.objects.create(
            hand=dealer_hand,
            value=3,
            img_url='?',
            position=2
        )
        controller.get_points(math)
        player_hand = models.Hand.objects.get(pk=player_hand.id)
        dealer_hand = models.Hand.objects.get(pk=dealer_hand.id)
        self.assertEqual(player_hand.total_point, 17)
        self.assertEqual(player_hand.is_out, False)
        self.assertEqual(dealer_hand.total_point, 23)
        self.assertEqual(dealer_hand.is_out, True)



