from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import ValidationError
from django.template.response import TemplateResponse
from django.test import TestCase, RequestFactory

from django_admin_smoke_tests.tests import AdminSiteSmokeTestMixin, for_all_model_admins


class ModRequestFactory(RequestFactory):
    """
    modifies the RequestFactory to not raise error when used in unittests.
    https://code.djangoproject.com/ticket/17971
    """

    def request(self, **request):
        req = super(ModRequestFactory, self).request(**request)
        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)
        return req


class AdminSiteSmokeTest(AdminSiteSmokeTestMixin, TestCase):
    """This automatically test all ModelAdmins registered in all apps other than `auth` """
    fixtures = []
    exclude_apps = ['auth', 'django_ses', ]

    def setUp(self):
        super(AdminSiteSmokeTest, self).setUp()
        self.factory = ModRequestFactory()

    @for_all_model_admins
    def test_change_post(self, model, model_admin):
        item = model.objects.last()
        if not item or model._meta.proxy:
            return
        pk = item.pk
        # TODO: If we generate default post_data for post request,
        # the test would be stronger
        request = self.post_request()
        try:
            response = model_admin.change_view(request, object_id=str(pk))
            if isinstance(response, TemplateResponse):
                response.render()
            self.assertIn(response.status_code, [200, 302])
        except ValidationError:
            # This the form was sent, but did not pass it's validation
            pass
