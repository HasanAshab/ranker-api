from django.core.management.base import BaseCommand
from api.users.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Update user ranks'

    def handle(self, *args, **kwargs):
        chunk_size = 1000 # as arg
        user = User.objects.all().order_by('-total_xp', '-date_joined')
        
        for i in range(0, len(user), chunk_size):
            users_chunk = user[i:i+chunk_size]
            self.update_user_ranks(users_chunk)

        self.stdout.write(self.style.SUCCESS('Ranks updated successfully'))

    def update_user_ranks(self, users_chunk):
        rank = 1
        prev_xp = None
        
        for user in users_chunk:
            if prev_xp is not None and user.total_xp < prev_xp:
                rank += 1
            user.rank = rank
            prev_xp = user.total_xp
        with transaction.atomic():
            User.objects.bulk_update(users_chunk, ['rank'])
