from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404
from django.test.client import RequestFactory
from django.test.testcases import SimpleTestCase

from django_dynamic_fixture import N
from mock import patch, Mock
from organizations.models import Organization
from signals.management import DECISION_CHANGE

# For some reason using relative imports throws an error
from publicweb.models import Decision
from publicweb.single_action_views import AddWatcher, RemoveWatcher


class WatcherViewTest(SimpleTestCase):

    @patch('publicweb.single_action_views.notification')
    def test_add_watcher_view_adds_observer_to_item(self, notifications):
        organization = N(Organization)
        decision = N(Decision, organization=organization)
        user = Mock(spec=User, id=1, organization_set=Mock(all=lambda: [organization]))

        view = AddWatcher()
        view.get_object = lambda: decision

        request = RequestFactory().get('/', {'next': '/'})
        request.user = user

        view.request = request
        view.get(request)

        notifications.observe.assert_called_with(
            decision, user, DECISION_CHANGE)

    @patch("publicweb.single_action_views.get_object_or_404")
    def test_get_object_tries_to_get_decision(self, decisions):
        view = AddWatcher()
        view.args = []
        view.kwargs = {'decision_id': 1}
        view.get_object()
        decisions.assert_called_with(Decision, pk=1)

    def test_get_user_looks_for_user_in_request(self):
        user = N(User)
        request = RequestFactory().get('')
        request.user = user
        view = AddWatcher()
        view.request = request

        self.assertEqual(user, view.get_user())

    @patch('publicweb.single_action_views.notification')
    def test_remove_watcher_view_removes_observer_from_item(self, notifications):
        organization = N(Organization)
        decision = N(Decision, organization=organization)
        user = Mock(spec=User, id=1, organization_set=Mock(all=lambda: [organization]))

        view = RemoveWatcher()
        view.get_object = lambda: decision

        request = RequestFactory().get('/', {'next': '/'})
        request.user = user

        view.request = request
        view.get(request)
        notifications.stop_observing.assert_called_with(decision, user)

    def test_add_watcher_view_requires_user_to_be_logged_in(self):
        decision = N(Decision)
        user = AnonymousUser()

        view = AddWatcher()
        view.get_object = lambda: decision

        request = RequestFactory().get('/', {'next': '/'})
        request.user = user

        response = view.dispatch(request)

        self.assertEqual('/accounts/login/?next=/%3Fnext%3D%252F', response['Location'])

    def test_remove_watcher_view_requires_user_to_be_logged_in(self):
        decision = N(Decision)
        user = AnonymousUser()

        view = RemoveWatcher()
        view.get_object = lambda: decision

        request = RequestFactory().get('/', {'next': '/'})
        request.user = user

        response = view.dispatch(request)

        self.assertEqual('/accounts/login/?next=/%3Fnext%3D%252F', response['Location'])

    def test_add_watcher_for_non_existant_item_returns_404(self):
        Decision.objects.all().delete()
        user = N(User)

        view = AddWatcher()

        request = RequestFactory().get('/', {'next': '/'})
        request.user = user

        self.assertRaises(Http404, view.dispatch, request, decision_id=1)

    def test_add_watcher_for_item_from_different_org_returns_404(self):
        Decision.objects.all().delete()
        organization = N(Organization)
        user = Mock(spec=User, id=1, organization_set=Mock(all=lambda: [organization]))
        decision = N(Decision)

        view = AddWatcher()
        view.get_object = lambda: decision

        request = RequestFactory().get('/', {'next': '/'})
        request.user = user

        self.assertRaises(Http404, view.dispatch, request, decision_id=1)

    def test_remove_watcher_for_item_from_different_org_returns_404(self):
        organization = N(Organization)
        user = Mock(spec=User, id=1, organization_set=Mock(all=lambda: [organization]))
        decision = N(Decision)

        view = RemoveWatcher()
        view.get_object = lambda: decision

        request = RequestFactory().get('/', {'next': '/'})
        request.user = user

        self.assertRaises(Http404, view.dispatch, request, decision_id=1)

