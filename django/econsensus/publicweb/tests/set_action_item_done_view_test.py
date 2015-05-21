from actionitems.models import ActionItem
from django.core.urlresolvers import reverse
from publicweb.tests.decision_test_case import DecisionTestCase

class SetActionItemDoneViewTest(DecisionTestCase):
    def test_invoking_view_marks_action_as_done(self):
        action = ActionItem(description='some action')
        