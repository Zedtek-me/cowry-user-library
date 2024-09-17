from django.core.management.base import BaseCommand
from AMQPs.consumer import LibraryConsumer


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("starting consumer with management command................")
        LibraryConsumer().consume_from_queue()
        