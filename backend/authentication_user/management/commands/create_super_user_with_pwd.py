from django.contrib.auth.management.commands.createsuperuser import Command as OrigCommand


class Command(OrigCommand):
    """
        Usage:
            zappa manage staging "create_super_user_with_pwd --email <su@mail.com> --no-input"
    """

    def handle(self, *args, **options):
        username = options[self.UserModel.USERNAME_FIELD]
        # generate random password
        pwd = self.UserModel.objects.make_random_password()
        self.UserModel.objects.create_superuser(username=username, email=username, password=pwd)
        self.stdout.write(f'Use the random password set to login and change afterwards: {pwd}')
