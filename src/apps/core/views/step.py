import json

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DeleteView

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView

from users.decorators import ForbiddenUser
from users.mixins import OwnerMixin
from users.forms import ConversationInviteForm

from ..forms import (
    StepCreateForm,
    StepUpdateForm,
    ChangePriorityForm,
)

from ..utils import (
    UpdateViewWrapper,
    DetailViewWrapper,
    ViewTypeWrapper,
    CommentsContentTypeWrapper,
    JsonView,
    DeleteViewWrapper,
)

from ..models import (
    Plan,
    Step,
    Task,
)

from ..utils import CreateViewWrapper
from ..filters import StepListViewFilter


class StepUpdateView(UpdateViewWrapper):

    """Step update view"""
    model = Step
    form_class = StepUpdateForm
    slug_field = "pk"
    template_name = "step/update.html"

    def form_valid(self, form):
        return super(StepUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully updated"))
        return reverse("plan-detail", args=[self.object.plan.pk, ])


class StepCreateView(CreateViewWrapper):

    """Step create view"""
    model = Step
    form_class = StepCreateForm
    template_name = "step/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.plan = Plan.objects.get(pk=self.kwargs['plan'])
        self.object.save()
        return super(StepCreateView, self).form_valid(form)

    def get_success_url(self):
        #messages.success(self.request, _("Step succesfully created"))
        return "%s?lang=%s" % (reverse("plan-detail", args=[self.object.plan.pk, ]), self.request.LANGUAGE_CODE)

    def get_context_data(self, **kwargs):
        context = super(StepCreateView, self).get_context_data(**kwargs)
        context.update({
                    'plan_object': Plan.objects.get(pk=self.kwargs['plan']),
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(StepCreateView, self).get_form_kwargs()
        kwargs['plan_instance'] = Plan.objects.get(pk=self.kwargs['plan'])
        kwargs['request'] = self.request
        return kwargs


class StepDeleteView(DeleteViewWrapper):

    """Step delete view"""
    model = Step
    slug_field = "pk"
    template_name = "step/delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Step succesfully deleted"))
        return reverse("plan-detail", args=[self.object.plan.pk, ])


class StepListView(ViewTypeWrapper, PaginationMixin, OrderableListMixin, ListFilteredView):

    template_name = "step/list.html"
    model = Step
    paginate_by = 1000
    orderable_columns = [
        "user",
        "name",
        "created_at",
        "updated_at",
        "deliverables",
        "priority",
        "plan",
        "objective",
        "investables",
    ]
    orderable_columns_default = "-id"
    filter_set = StepListViewFilter

    def get_base_queryset(self):
        queryset = super(StepListView, self).get_base_queryset()
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset


class StepDetailView(DetailViewWrapper, CommentsContentTypeWrapper):

    """Step detail view"""
    model = Step
    slug_field = "pk"
    template_name = "step/detail.html"

    def get_success_url(self):
        messages.success(
            self.request, _(
                "%s succesfully created" %
                self.form_class._meta.model.__name__))
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(StepDetailView, self).get_context_data(**kwargs)

        context.update({
            'task_list': Task.objects.filter(step=kwargs.get('object')).order_by('id')
        })

        return context


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class ChangeStepPriorityView(JsonView):
    def post(self, request, *args, **kwargs):
        form = ChangePriorityForm(request.POST)

        username = request.GET.get('user', None)

        if form.is_valid():
            steps = json.loads(form.data.get('steps'))
            for step in steps:
                try:
                    step_instance = Step.objects.get(id=step['id'])

                    if not step_instance.plan.user == request.user and request.user not in step_instance.plan.members.all():
                        return self.json({'error': True, 'message': 'Access error'})

                    if username:
                        """ only change Step.user_priority"""
                        step_instance.user_priority = step['index']
                        print "changing user priority"
                    else:
                        """ change Step.priority """
                        step_instance.priority = step['index']

                    step_instance.save()
                    data = {'error': False}
                except Step.DoesNotExist as e:
                    data = {'error': True, 'message': e.message}
        else:
            data = {'error': True, 'message': form.errors }

        return self.json(data)
