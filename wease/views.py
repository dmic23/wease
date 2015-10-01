from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from orders.models import Good
from django.utils.decorators import method_decorator


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):

        return super(IndexView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['goods'] = Good.objects.all()
        return context
