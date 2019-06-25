from django.core.management.base import BaseCommand

from project.utils import generate_sales


class Command(BaseCommand):

    def handle(self, *args, **options):
        sales = generate_sales()
        self.stdout.write(self.style.SUCCESS('Created {} objects.'.format(len(sales))))
