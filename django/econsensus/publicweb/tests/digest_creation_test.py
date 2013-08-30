from django.test.testcases import TestCase
from django_dynamic_fixture import N
from django.contrib.auth.models import User
from notification.models import ObservedItem
from publicweb.models import Decision
from minimock import mock, Mock
from publicweb.digest_managers import EmailDigestManager
from digested.digest_managers import BaseDigestManager
from digested.models import PREFERENCE_DAILY

class DigestCreationTest(TestCase):
    def setUp(self):
        self.users = N(User, n=5)
        self.decisions = N(Decision, n=2)
        objects = Mock('Decision.objects')
        objects.all = self._decision_list

        mock('Decision.objects', mock_obj=objects)
        for index, user in enumerate(self.users):
            user.id = index
        for index, decision in enumerate(self.decisions):
            decision.id = index
        self.observed_items = [[
           N(ObservedItem, observed_object=self.decisions[0], user=user) 
               for user in self.users[:3]],
           [N(ObservedItem, observed_object=self.decisions[1], user=user) 
               for user in self.users[3:]]
               ]
        self.decisions[0].watchers = self.observed_items[0]
        self.decisions[1].watchers = self.observed_items[1]
    
    def _decision_list(self):
        return self.decisions
    
    def test_digest_manager_is_a_subclass_of_base_digest_manager(self):
        the_manager = EmailDigestManager()
        self.assertIsInstance(the_manager, BaseDigestManager)
        
    def test_get_items_returns_decisions(self):
        the_manager = EmailDigestManager()
        actual_items = the_manager.get_items()
        expected_items = Decision.objects.all()
        self.assertSequenceEqual(expected_items, actual_items)
    
    def test_digest_manager_default_preference_is_daily(self):
        the_manager = EmailDigestManager()
        self.assertEqual(PREFERENCE_DAILY, the_manager.default_preference)
    
    def test_subscribers_for_a_decision_are_the_watchers(self):
        the_manager = EmailDigestManager()
        decision = Decision.objects.all()[0]
        subscribers = the_manager.get_subscribers_for_item(decision)
        expected_subscribers = [(subscription.object_id, subscription.user_id)
                                for subscription in self.observed_items[0]]
        actual_subscribers = [(subscription.object_id, subscription.user_id)
                                for subscription in subscribers] 
        self.assertSequenceEqual(expected_subscribers, actual_subscribers)