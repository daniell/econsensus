from publicweb.models import Decision
from digested.digest_managers import BaseDigestManager
from digested.models import PREFERENCE_DAILY

class EmailDigestManager(BaseDigestManager):
    default_preference = PREFERENCE_DAILY
    
    def get_items(self):
        return Decision.objects.all()
    
    def get_subscribers_for_item(self, item):
        return item.watchers.all()