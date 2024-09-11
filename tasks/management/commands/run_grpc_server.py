from django.core.management.base import BaseCommand
from tasks.grpc_server import serve

class Command(BaseCommand):
    help = 'Start gRPC server'

    def handle(self, *args, **kwargs):
        serve()
