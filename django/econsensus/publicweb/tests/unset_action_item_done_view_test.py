from django.contrib.auth.models import AnonymousUser, User
from django.test.client import RequestFactory
from django.test.testcases import TestCase

from actionitems.models import ActionItem
from mock import Mock, patch

from publicweb.single_action_views import UnsetActionItemDone
from django.conf import settings


class UnsetActionItemDoneViewTest(TestCase):
    @patch('publicweb.single_action_views.ActionItem.save', new=Mock())
    def test_invoking_view_marks_action_as_not_done(self):
        action = ActionItem(description='some action', id=1)
        action.done = True

        view = UnsetActionItemDone()

        request = RequestFactory().get('/', {'next': '/'})
        request.user = User()
        view.get_object = lambda: action

        view.dispatch(request, action.id)
        self.assertFalse(action.done)

    def test_view_requires_login(self):
        view = UnsetActionItemDone()

        request = RequestFactory().get('/')
        request.user = AnonymousUser()

        response = view.dispatch(request, 1)

        self.assertEqual(settings.LOGIN_URL + '?next=/', response['Location'])