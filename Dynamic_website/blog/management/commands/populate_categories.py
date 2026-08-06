from typing import Any
from blog.models import Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command for insert categories data"

    def handle(self, *args: Any, **options: Any):

        # delete existing data
        Category.objects.all().delete()

        categories = ['sports', 'Technology', 'Science', 'Art', 'Food']

        for categories_name in categories:
             Category.objects.create(name = categories_name)

        self.stdout.write(self.style.SUCCESS("COMPLETED INSERTING DATA"))