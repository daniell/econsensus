from publicweb.models import Decision
from digested.digest_managers import BaseDigestManager

class EmailDigestManager(BaseDigestManager):
    def get_items(self):
        return Decision.objects.all()