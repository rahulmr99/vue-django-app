from django.test import RequestFactory
from django.urls import reverse
from utils_plus.utils import reverse_url

from mailer import tasks
from ratings_manager.models import Feedback


def test_sending_feedback_email(past_monday_appointment, mailoutbox):
    mailoutbox.clear()
    tasks.send_feedback_emails()  # send feedback mail to customer
    assert len(mailoutbox) == 1
    assert '/feedback/get/' in mailoutbox[0].body


def test_thanks_page(rf: RequestFactory):
    # Issue a GET request.
    rf.get(str(reverse_url('feedback:thank-you')))


def test_get_feedback_form_positive(past_monday_appointment, client):
    token = past_monday_appointment.get_encoded_token()
    url_auth = reverse_url('feedback:get-feedback', token, 5)
    # Check URL with tokens
    response = client.get(url_auth)
    assert Feedback.objects.count() == 1
    assert 'Yelp or Google if you haven' in str(response.content)


def test_get_feedback_form_negative(past_monday_appointment, client):
    token = past_monday_appointment.get_encoded_token()
    url_auth = reverse_url('feedback:get-feedback', token, 2)
    # Check URL with tokens
    response = client.get(url_auth)
    assert 'Please tell us more about your experience' in str(response.content)

    # issue a post request
    response = client.post(url_auth, {'content': 'some feedback text'})
    assert Feedback.objects.count() == 1
    assert Feedback.objects.first().calendardb.pk == past_monday_appointment.pk
    assert response.status_code == 302
    assert response.url == reverse('feedback:thank-you')
