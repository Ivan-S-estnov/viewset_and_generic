from django.core.management import BaseCommand

from materials.models import Course, Lesson

class Command(BaseCommand):

    def handle(self, *args, **option):
        """ Create course and lesson"""

        course1, _ = Course.objects.get_or_create(name="Литература",
                       description="Произведения письменности, имеющие общественное, познавательное значение")

        lessons =[
            {
            "name": "Художественная литература",
            "description": "Вид искусства, в котором мысли, чувства и идеи автора выражаются через художественный язык",
            "course": course1
            },
            {
            "name": "Научная литература",
            "description": "Письменные труды, созданные в результате исследований и теоретических обобщений",
            "course": course1
            }
        ]

        for lesson_data in lessons:
            lesson, created = Lesson.objects.get_or_create(**lesson_data)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully added product: {lesson.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Product already exist: {lesson.name}'))
