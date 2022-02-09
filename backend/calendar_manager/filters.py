from django_filters import rest_framework
from . import models


class CalendarDbFilter(rest_framework.FilterSet):
    class Meta:
        model = models.CalendarDb
        fields = {
            # from the table itself
            'book_datetime': ['date', 'exact', ],
            'start_datetime': ['date', 'exact', ],
            'end_datetime': ['date', 'exact', ],
            'uid': ['exact', ],
            'generalsettings': ['exact', ],

            # from the provider
            'users_provider__name': ['icontains', 'exact', ],
            'users_provider__last_name': ['icontains', 'exact', ],
            'users_provider__email': ['icontains', 'exact', ],
            'users_provider__phone': ['icontains', 'exact', ],
            'users_provider__mobile': ['icontains', 'exact', ],
            'users_provider__state': ['exact', ],
            'users_provider__city': ['exact', ],
            'users_provider__country': ['exact', ],
            'users_provider__zip_code': ['exact', ],

            # from the customer
            'users_customer__name': ['icontains', 'exact', ],
            'users_customer__last_name': ['icontains', 'exact', ],
            'users_customer__email': ['icontains', 'exact', ],
            'users_customer__phone': ['icontains', 'exact', ],
            'users_customer__mobile': ['icontains', 'exact', ],
            'users_customer__state': ['exact', ],
            'users_customer__city': ['exact', ],
            'users_customer__country': ['exact', ],
            'users_customer__zip_code': ['exact', ],

            # from the service
            'services__name': ['exact', 'icontains', ],
            'services__description': ['exact', 'icontains', ],
        }
