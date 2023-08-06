from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .forms import UnsubscribeForm
from .models import Status


class UnsubscribeView(FormView):
    template_name = 'email-notifications/unsubscribe.html'
    form_class = UnsubscribeForm
    success_url = reverse_lazy('unsubscribe_done')

    _status = None

    def dispatch(self, request, *args, **kwargs):
        self._status = get_object_or_404(
            Status,
            uuid=self.kwargs['uuid'],
            status=Status.SUBSCRIBE,
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self._status.unsubscribe()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'user': self._status.user})
        return context


class UnsubscribeDoneView(TemplateView):
    template_name = 'email-notifications/unsubscribe_done.html'
