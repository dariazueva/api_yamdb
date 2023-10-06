from django.core.mail import send_mail


class Util:
    def send_mail(email, confirmation_code):
        """Отправка сообщений с кодом подтверждения на почту."""

        send_mail(
            subject='Yamdb confirmation code',
            message=f'Ваш проверочный код: {confirmation_code}',
            from_email='yamdb@yandex.ru',
            recipient_list=[email],
            fail_silently=False)
