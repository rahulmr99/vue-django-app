from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string

from .querysets import AccountQuerySet


class AccountManager(BaseUserManager):
    def get_queryset(self):
        return AccountQuerySet(self.model, using=self._db, hints=self._hints)

    def create_customer(self, email, password=None, **kwargs):
        if not password:
            password = get_random_string(6)

        account = self.model(email=self.normalize_email(email))

        if 'generalsettings_id' in kwargs:
            account.generalsettings_id = kwargs['generalsettings_id']

        account.name = kwargs.get('name', None)
        account.last_name = kwargs.get('last_name', None)
        account.phone = kwargs.get('phone', '-')
        account.address = kwargs.get('address', '-')
        account.city = kwargs.get('city', '-')
        account.zip_code = kwargs.get('zip_code', '-')
        account.is_admin = kwargs.get('is_admin', False)
        account.is_root_user = kwargs.get('is_root_user', False)
        account.is_customers = True
        account.is_active = None
        account.set_password(password)
        account.note = kwargs.get('note', '-')
        account.save(using=self._db)

        return account

    def create_user(self, **kwargs):
        if ('email' in kwargs
                and kwargs['email']
                and self.filter(email=kwargs['email'], is_active=True).exists()):
            raise ValueError('The fields email, is_active must make a unique set.')
        if ('generalsettings_id' in kwargs
                and 'email' in kwargs
                and self.filter(generalsettings_id=kwargs['generalsettings_id'], email=kwargs['email']).exists()):
            raise ValueError('The fields generalsettings, email must make a unique set.')
        if ('generalsettings_id' in kwargs
                and self.filter(generalsettings_id=kwargs['generalsettings_id'], phone=kwargs.get('phone'),
                                country=kwargs.get('country')).exists()):
            raise ValueError('The fields generalsettings, phone, country must make a unique set.')
        password = kwargs.pop('password', None)
        account = self.model(**kwargs)
        if password is not None:
            account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, *args, **kwargs):
        """to match abstract user manager class's function signature"""
        username, email, password = None, None, None
        if len(args) == 3:
            username, email, password = args
        elif len(args) == 2:
            username, email = args
        elif len(args) == 1:
            username = args[0]

        name = kwargs.get('name') or kwargs.pop('first_name', None) or username or kwargs.get('email')

        for k, v in dict(
            username=username,
            email=email,
            password=password,
            name=name,
            is_admin=True,
            is_root_user=True,
            is_active=True,
            is_superuser=True,
            is_staff=True,
        ).items():
            kwargs.setdefault(k, v)

        return self.create_user(**kwargs)

    def create_restore_token(self, email):
        user = self.get_queryset().get(email=email)
        user.token = get_random_string(50)
        user.restore = True
        user.save()
        return user

    def remove_token(self, token, password):
        user = self.get_queryset().get(token=token)
        user.token = ''
        user.restore = False
        user.set_password(password)
        user.save()
        return user

    def delete_user(self, id):
        account = self.get_queryset().get(id=id)
        account.delete()
        return account

    def update_user(self, id, context, password=None):
        password = context.pop('password', None) or password
        account = self.get_queryset().filter(id=id).update(**context)
        if password:
            user = self.get_queryset().get(id=id)
            user.set_password(password)
            user.save()
        return account

    def update_password(self, id, password=None):
        if password:
            user = self.get_queryset().get(id=id)
            user.set_password(password)
            user.save()
            return user

    def get_by_natural_key(self, username):
        # todo: Create a separate model for ProviderAccount and avoid this override
        # this method is used by Auth backend and we should authenticate only ProviderAccount.
        return self.get_queryset().authorizables().get(**{self.model.USERNAME_FIELD: username})


class ProviderAccountManager(AccountManager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.providers()


class CustomerAccountManager(AccountManager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.customers()
