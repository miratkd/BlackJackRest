from app1 import models, exceptions
import datetime
from random import randint


def redeem_free_daily_tickets(user):
    already_redeem = models.DailyFreeTicket.objects.filter(account=user.account, date=datetime.datetime.now().date())
    if len(already_redeem) > 0:
        raise exceptions.AlreadyRedeemDailyCode
    user.account.tickets += 200
    user.account.save()
    models.DailyFreeTicket.objects.create(
        account=user.account,
        date=datetime.datetime.now().date()
    )
    return user


def create_card(hand, position):
    card_value = randint(1, 13)
    card_naipe = randint(1, 4)

    if card_value == 1:
        url = 'ace'
    elif 1 < card_value < 11:
        url = str(card_value)
    elif card_value == 11:
        url = 'jack'
    elif card_value == 12:
        url = 'queen'
    else:
        url = 'king'

    if card_naipe == 1:
        url += '_of_clubs.svg'
    elif card_naipe == 2:
        url += '_of_diamonds.svg'
    elif card_naipe == 3:
        url += '_of_hearts.svg'
    else:
        url += '_of_spades.svg'

    if card_value > 10:
        card_value = 10

    return models.Card.objects.create(
        hand=hand,
        value=card_value,
        position=position,
        img_url=url
    )


def get_points(math):
    hands = models.Hand.objects.filter(math=math, round=math.active_round)
    for hand in hands:
        all_cards = models.Card.objects.filter(hand=hand)
        total_value = 0
        number_of_aces = 0
        for card in all_cards:
            if card.value == 1:
                number_of_aces += 1
                total_value += 11
            else:
                total_value += card.value
        if total_value > 21:
            for t in range(number_of_aces):
                total_value -= 10
                if total_value < 22:
                    break
        if total_value > 21:
            hand.is_out = True
        hand.total_point = total_value
        hand.save()


def draw_player_card(math):
    hand = models.Hand.objects.get(math=math, round=math.active_round, is_player_hand=True)
    if hand.is_out or hand.is_hold:
        raise exceptions.IsOutException
    create_card(hand, len(models.Card.objects.filter(hand=hand)) + 1)
    get_points(math)


def next_round(math):
    if math.active_round >= 5:
        if math.rounds_won == 5:
            math.is_over = True
            math.is_win = True
            math.account.tickets += math.prize
            math.account.save()
            math.save()
            raise exceptions.MathIsOverException(is_player_win=True)
        elif math.active_round - math.rounds_won == 5:
            math.is_over = True
            math.save()
            raise exceptions.MathIsOverException(is_player_win=False)

    math.active_round += 1
    math.save()

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
        create_card(player_hand, number)
    for number in [1, 2]:
        create_card(dealer_hand, number)
    get_points(math)
    return math


def draw_dealer_card(math, player_points):
    dealer_hand = models.Hand.objects.get(math=math, round=math.active_round, is_player_hand=False)
    if dealer_hand.is_out:
        math.rounds_won += 1
        math.save()
        return True, math
    if dealer_hand.total_point >= player_points:
        return False, math
    create_card(dealer_hand, len(models.Card.objects.filter(hand=dealer_hand)) + 1)
    get_points(math)
    return draw_dealer_card(math, player_points)


def hold_round(math):
    player_hand = models.Hand.objects.get(math=math, round=math.active_round, is_player_hand=True)
    if player_hand.is_hold:
        raise exceptions.AlreadyHoldException
    if player_hand.is_out:
        return False, math
    player_hand.is_hold = True
    player_hand.save()
    return draw_dealer_card(math, player_hand.total_point)


def user_is_authorized(user, math):
    if not math.account.user == user:
        raise exceptions.UnauthorizedPlayerException


