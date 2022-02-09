class GetGenSettingsMixin(object):
    """this will help filtering the queryset based on
    1. user logged in
    2. GET parameter

    This should be used with a viewset
    """

    def get_queryset(self):
        fltrs = {}
        if self.request.user.is_authenticated:
            fltrs['generalsettings_id'] = self.request.user.generalsettings_id
        elif str(self.request.GET.get('generalsettings')).isdigit():
            fltrs['generalsettings_id'] = self.request.GET.get('generalsettings')
        elif hasattr(self.request, 'data') and str(self.request.data.get('generalsettings')).isdigit():
            fltrs['generalsettings_id'] = self.request.data['generalsettings']
        return super(GetGenSettingsMixin, self).get_queryset().filter(**fltrs)
