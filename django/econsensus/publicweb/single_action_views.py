from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from actionitems.models import ActionItem
from notification import models as notification
from signals.management import DECISION_CHANGE

from .models import Decision
from guardian.mixins import PermissionRequiredMixin, LoginRequiredMixin
from socket import meth


class BaseSingleActionView(LoginRequiredMixin, View):
    """ SingleActionViews are views used to perform a single, simple
        action such as marking an item as done. This used with a
        redirection to provide quick, one-click actions that do
        not require javascript.

        - Users need to provide a URL route to the single action view;
        - Descendant classes should implement a single 'do_action'
        method to perform the action;
        - Requests are expected to contains a GET parameter 'next' then the
        user will be redirected to the given URL.
    """
    def get(self, request, *args, **kwargs):
        self.do_action()
        return HttpResponseRedirect(request.GET['next'])


class BaseWatcherView(BaseSingleActionView):
    """ Base single action view for add/remove watcher views """
    def get_object(self):
        object_id = self.kwargs['decision_id']
        decision = Decision.objects.get(pk=object_id)
        return decision

    def get_user(self):
        return self.request.user


class BaseActionItemView(BaseSingleActionView):
    """ Base single action view for set/unset action item done views """
    def get_object(self):
        object_id = self.kwargs['actionitem_id']
        actionitem = get_object_or_404(ActionItem, pk=object_id)
        return actionitem


class AddWatcher(BaseWatcherView):
    """ Single action view used to add a new watcher to a decision """
    def do_action(self):
        decision = self.get_object()
        user = self.get_user()
        notification.observe(decision, user, DECISION_CHANGE)


class RemoveWatcher(BaseWatcherView):
    """ Single action view used to remove a watcher from a decision """
    def do_action(self):
        decision = self.get_object()
        user = self.get_user()
        notification.stop_observing(decision, user)


class SetActionItemDone(BaseActionItemView):
    """ Single action view used to set an action item as done """
    def do_action(self):
        actionitem = self.get_object()
        actionitem.done = True
        actionitem.save()


class UnsetActionItemDone(BaseActionItemView):
    """ Single action view used to unset an action item's done status """
    def do_action(self):
        actionitem = self.get_object()
        actionitem.done = False
        actionitem.save()
