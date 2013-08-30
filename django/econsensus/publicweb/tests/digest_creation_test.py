from django.test.testcases import TestCase
from django_dynamic_fixture import N
from django.contrib.auth.models import User
from notification.models import ObservedItem
from publicweb.models import Decision
from minimock import mock, Mock
from publicweb.digest_managers import EmailDigestManager

class DigestCreationTest(TestCase):
    def setUp(self):
        self.users = N(User, n=5)
        self.decisions = N(Decision, n=2)
        objects = Mock('Decision.objects')
        objects.all = self.decision_list

        mock('Decision.objects', mock_obj=objects)
        for index, user in enumerate(self.users):
            user.id = index
        for index, decision in enumerate(self.decisions):
            decision.id = index
        self.observed_items = [[
           N(ObservedItem, decision=self.decisions[0], user=user) 
               for user in self.users[:3]],
           [N(ObservedItem, decision=self.decisions[1], user=user) 
               for user in self.users[3:]]
               ]
        self.decisions[0].watchers = self.observed_items[0]
        self.decisions[1].watchers = self.observed_items[1]
    
    def decision_list(self):
        return self.decisions
    
    def test_get_items_returns_decisions(self):
        the_manager = EmailDigestManager()
        actual_items = the_manager.get_items()
        expected_items = Decision.objects.all()
        self.assertSequenceEqual(expected_items, actual_items)
        