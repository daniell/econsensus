from publicweb.models import Decision

class EmailDigestManager(object):
    def get_items(self):
        return Decision.objects.all()