from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView

from app_settings.models import FeedbackConfig
from calendar_manager.models import CalendarDb
from ratings_manager.models import Feedback
from ratings_manager.utils import decode_calendar
from .forms import FeedbackForm


class ThanksView(TemplateView):
    """
        After getting feedback show thanks message
    """
    template_name = 'feedback/thank-you.html'


class ReportsView(LoginRequiredMixin, TemplateView):
    """
        Show a report on feedbacks
    """
    template_name = 'feedback/reports.html'

    def get_context_data(self, **kwargs):
        ctx = super(ReportsView, self).get_context_data(**kwargs)
        ratings = []
        total = Feedback.objects.count()
        for i in range(1, 6):
            rating = {'name': i}
            rating['count'] = count = Feedback.objects.filter(rating_given=i).count()
            rating['percent'] = round(((count / total) * 100), 2)
            ratings.append(rating)
        ctx['ratings'] = ratings
        return ctx


@method_decorator(csrf_exempt, name='dispatch')
class GetFeedback(FormView):
    """
        show the feedback form and create a feedback record after submission
    """
    success_url = reverse_lazy('feedback:thank-you')
    form_class = FeedbackForm

    def get_template_names(self):
        rating = int(self.kwargs.get('rating') or 0)
        if rating > 3:
            # keep track of this feedback by creating record unique.
            feedback = Feedback.objects.filter(calendardb=self.calendardb, rating_given=rating).first()
            if not feedback:
                Feedback.objects.create(calendardb=self.calendardb, rating_given=rating)

            # user has rated positively and we thank them and suggest to rate us on yelp and google.
            return ['feedback/review-us.html']
        # get feedback in a form
        return ['feedback/tell-us-more.html']

    def get_context_data(self, **kwargs):
        ctx = super(GetFeedback, self).get_context_data(**kwargs)
        self.kwargs.update(kwargs)
        ctx['feedbackconfig'] = FeedbackConfig.objects.get(
            generalsettings_id=self.calendardb.generalsettings_id
        )
        return ctx

    @cached_property
    def calendardb(self):
        """

        Returns:
            CalendarDb:
        """
        calendardb = decode_calendar(self.kwargs.get('token'))
        if not calendardb:
            raise Http404
        return calendardb

    def form_valid(self, form):
        """
            once the form is submitted create feedback record from the POST data
        Args:
            form (FeedbackForm):

        Returns:

        """
        form.clean()
        feedback = form.instance
        feedback.calendardb = self.calendardb
        feedback.rating_given = self.kwargs.get('rating')
        feedback.save()
        return super(GetFeedback, self).form_valid(form)
