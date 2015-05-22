from django.http import Http404
from actionitems.models import ActionItem
import decorators


class is_org_member(decorators.FuncDecorator):

    def decorate_func(self, func, *args, **kwargs):
        def wrapped_func(self, request, *args, **kwargs):
            item = self.get_object()
            if(isinstance(item, ActionItem)):
                org = item.origin.organization
            else:
                org = item.organization

            if org in request.user.organization_set.all():
                return func(self, request, *args, **kwargs)
            else:
                raise Http404
        return wrapped_func
