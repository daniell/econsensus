from django.core.urlresolvers import reverse
from publicweb.tests.decision_test_case import DecisionTestCase
from publicweb.models import Feedback

# TODO: Check that POSTs save correct data and redirects work
class ViewDecisionTest(DecisionTestCase):
    def test_view_decision(self):
        decision = self.create_and_return_decision()
        response = self.client.get(reverse('publicweb_decision_detail', args=[decision.id]))
        self.assertContains(response, u"Proposal")
        self.assertContains(response, decision.description)
        self.assertContains(response, u'<rect width="9"')

    def test_view_feedback(self):
        decision = self.create_and_return_decision()
        feedback = Feedback(description='test feedback',
                          decision=decision)
        feedback.save()
        response = self.client.get(reverse('publicweb_feedback_detail', args=[feedback.id]))
        self.assertContains(response, u"Feedback")
        self.assertContains(response, feedback.description)

    def test_load_decision_snippet(self):
        decision = self.create_and_return_decision()
        response = self.client.get(reverse('publicweb_decision_view_snippet', args=[decision.id]))

        self.assertContains(response, u'<a href="/view/%s/edit/">Edit</a>' % decision.id)
        self.assertTrue(response.content.strip().startswith('<div id="decision">'))
        self.assertContains(response, u'<rect width="9"')

    def test_load_form_snippet(self):
        form_fields = set(['status', 'review_date', 'description', 'tags', 'budget', 'effective_date', 'csrfmiddlewaretoken', 'decided_date'])
        decision = self.create_and_return_decision()
        response = self.client.get(reverse('inline_edit_decision_form', args=[decision.id]))

        self.assertTrue(response.content.strip().startswith('<form action="#" method="post" class="edit_decision_form">'))

        form_data = self.get_form_values_from_response(response, 1)
        self.assertTrue(form_fields.issubset(set(form_data.keys())))

    def test_load_decision_form(self):
        form_fields = set(['status', 'review_date', 'description', 'tags', 'budget', 'effective_date', 'csrfmiddlewaretoken', 'decided_date'])
        decision = self.create_and_return_decision()
        response = self.client.get(reverse('inline_edit_decision', args=[decision.id]))
        response_content = response.content.strip()

        self.assertFalse(response_content.startswith('<form action="#" method="post" class="edit_decision_form">'))
        self.assertTrue(response_content.startswith('<!DOCTYPE html'))
        self.assertContains(response, u"Edit proposal: <span>%s</span>" % decision.excerpt)

        form_data = self.get_form_values_from_response(response, 2)
        self.assertTrue(form_fields.issubset(set(form_data.keys())))