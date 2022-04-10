from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tickets = models.IntegerField(help_text="Saldo de tickets da conta.")

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"

    def __str__(self):
        return self.user.email

    def delete(self, using=None, keep_parents=False):
        self.user.delete()


class DailyFreeTicket(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='conta')
    date = models.DateField(verbose_name='dia do resgate')

    class Meta:
        verbose_name_plural = "Tickets diarios"
        verbose_name = "Ticket diario"

    def __str__(self):
        return self.account.user.email + '-' + self.date.strftime('%d/%m/%Y')


class Coupon(models.Model):
    code = models.CharField(max_length=50, help_text='Limite de 50 characteres.', unique=True, verbose_name='codigo')
    valid_until = models.DateField(verbose_name='Valido ate')
    prize = models.IntegerField(verbose_name='Recompensa')
    is_active = models.BooleanField(default=True, help_text='desative essa opcao ao inves de deletar o objeto.',
                                    verbose_name='ativado')

    class Meta:
        verbose_name_plural = "Cupoms"
        verbose_name = "Cupom"

    def __str__(self):
        return self.code


class CouponHistory(models.Model):
    coupon = models.ForeignKey(to=Coupon, related_name='accounts', on_delete=models.PROTECT, verbose_name='cupom')
    account = models.ForeignKey(to=Account, related_name='coupons', on_delete=models.CASCADE, verbose_name='conta')

    class Meta:
        verbose_name_plural = "historico de cupons"
        verbose_name = "resgate de cupon"

    def __str__(self):
        return self.account.user.username + ' - ' + str(self.coupon)


class Math(models.Model):
    prize = models.IntegerField(verbose_name='premio')
    date = models.DateTimeField(verbose_name='data')
    account = models.ForeignKey(to=Account, related_name='maths', verbose_name='conta', on_delete=models.CASCADE)
    is_win = models.BooleanField(default=False, verbose_name='ganhou')
    rounds_won = models.IntegerField(verbose_name='rounds ganhos.')
    is_over = models.BooleanField(default=False, verbose_name='partida finalizada')
    math_active_round = models.IntegerField(verbose_name='round ativo')

    class Meta:
        verbose_name_plural = "partidas"
        verbose_name = "partida"

    def __str__(self):
        return self.account.user.username + ' - ' + self.date.strftime('%d/%m/%Y')


class Hand(models.Model):
    round = models.IntegerField()
    math = models.ForeignKey(to=Math, related_name='rounds', verbose_name='partida', on_delete=models.CASCADE)
    total_point = models.IntegerField(verbose_name='pontos')
    is_out = models.BooleanField(verbose_name='bateu')
    is_player_hand = models.BooleanField(verbose_name='jogador')
    is_hold = models.BooleanField(default=False, verbose_name='parou')

    class Meta:
        verbose_name_plural = "maos"
        verbose_name = "mao"

    def __str__(self):
        return str(self.math) + ' - round: ' + str(self.round)


class Card(models.Model):
    hand = models.ForeignKey(to=Hand, related_name='cards', verbose_name='mao', on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name='valor')
    img_url = models.CharField(max_length=50)
    position = models.IntegerField(verbose_name='posicao')

    class Meta:
        verbose_name_plural = "maos"
        verbose_name = "mao"

    def __str__(self):
        return str(self.value)

