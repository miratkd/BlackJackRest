class AlreadyRedeemDailyCode(Exception):
    message = "have you redeemed your daily tickets today."


class NotEnoughTicketsException(Exception):
    message = 'You doest have enough tickets for this actions'
    points_available = 0
    points_needed = 0

    def __init__(self, available, needed):
        self.points_available = available
        self.points_needed = needed


class IsOutException(Exception):
    message = 'You can not draw another card, this round is over.'


class MathIsOverException(Exception):
    message = ''

    def __init__(self, is_player_win):
        if is_player_win:
            self.message = 'Congratulations! you won the math!'
        else:
            self.message = 'Sorry, you lose the math.'


class AlreadyHoldException(Exception):
    message = 'You cant hold again'


class UnauthorizedPlayerException(Exception):
    message = 'You cant play another player math'

