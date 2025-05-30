from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):


    def handle(self, *args, **options):
        """Create user and payments"""

        user1, user_status = User.objects.get_or_create(email='favor@example.ru', password='7283')
        user1.is_staff = True
        user1.is_superuser = True
        user1.save()
        print('User created successfully.')

        payments =[
            {
        'user': user1,
        'payment_date': '2022-08-21',
        'paid_course': Course.objects.get(pk=1),
        'paid_lesson': None,
        'amount': 2300,
        'method': 'наличные'
    },
        {
            'user': user1,
            'payment_date': '2023-02-15',
            'paid_course': Course.objects.get(pk=1),
            'paid_lesson': Lesson.objects.get(pk=1),
            'amount': 2550,
            'method': 'перевод'
        },
        {
            'user': user1,
            'payment_date': '2024-06-17',
            'paid_course': Course.objects.get(pk=1),
            'paid_lesson': Lesson.objects.get(pk=2),
            'amount': 1750,
            'method': 'перевод'
        }
        ]
        [Payment.objects.create(**payment) for payment in payments]
        print('Payment created successfully.')
