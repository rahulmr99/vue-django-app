import sys
import time

import os
import shutil
from datetime import datetime
from fabric.api import *
from fabric.colors import blue, red, green, magenta

env.hosts = ['ubuntu@ec2-18-217-189-234.us-east-2.compute.amazonaws.com']
env.key_filename = './.local/keys/easybookingapp3.pem'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

PROJECT_NAME = 'bookedfusion'
PROJECT_FOLDER = '/home/ubuntu/easy_appointments_back'
VENV_CMD = 'source /home/ubuntu//miniconda3/bin/activate'
PROMPTS = {}
env.code_repo = 'git@bitbucket.org:mlaurenzi/easy_appointments_backend.git'
env.environment = 'staging'
env.branch = 'master'
env.user = 'www-data'
env.user_group = 'www-data'


def blue_caption(caption):
    print(blue("{}".format(caption)))


def green_caption(caption):
    print(green("{}".format(caption)))


def red_caption(*args):
    print(red(*args))


@task
def ssh():
    local(f"ssh -i {env.key_filename} {env.hosts[0]}")


@task
def loaddata(*apps):
    """
        load data from server and remove all local data
    Args:
        *apps: name of the app to load data. Empty one will load all data
    """
    import sys, os
    sys.path.insert(0, os.path.abspath(os.curdir))
    from backend.settings.base import PROJECT_LIST
    apps = apps or PROJECT_LIST

    filename = "dump.tar.gz"
    with prefix(VENV_CMD), cd(PROJECT_FOLDER):
        run(
            "./manage.py dumpdata {} "
            "-e contenttypes "
            "-e sessions "
            "-e admin "
            "-e auth "
            # "--natural-foreign "
            "-o dump.json".format(" ".join(apps)))
        run("tar -czvf {} dump.json".format(filename))
        run("rm dump.json")
        get(filename, '.')
        run("rm {}".format(filename))
    local("tar -xzvf {} dump.json".format(filename))
    local("rm {}".format(filename))
    for app in apps:
        local("python manage.py cleardata %s" % app)
    local("python manage.py loaddata dump.json")
    local('rm dump.json')


@task
def apt():
    """install ubuntu packages needed for project"""
    sudo('apt-get update')
    sudo('apt-get install build-essential libssl-dev libffi-dev python3-dev libgdal-dev -y')
    # for python audio libraries pydubs/speechrecognition
    sudo('apt-get install swig libpulse-dev ffmpeg -y')

    # libav for pydub
    sudo('apt-get install libav-tools libavcodec-extra')


@task
def pip():
    with prefix(VENV_CMD), cd(PROJECT_FOLDER):
        run("pip install -r requirements.txt")


@task
def clean():
    """Cleans Python bytecode"""
    cmd = """find . -name "*.pyc"|xargs rm -rf"""
    local(cmd)
    local("./manage.py clean_pyc")

    with prefix(VENV_CMD), cd(PROJECT_FOLDER):
        run(cmd)
        run("python manage.py clean_pyc")


@task
def push():
    """
    Push source code to server
    """
    # check we are in the correct local branch
    current_branch_name = local('git rev-parse --abbrev-ref HEAD', capture=True)
    assert current_branch_name.strip() == env.branch

    local('git push')
    with cd(PROJECT_FOLDER):
        run('git checkout {}'.format(env.branch))
        run('git tag depl_{}'.format(datetime.now().strftime('%d%m%y.%H%M%S')))
        run('git pull')


@task
def check():
    """checks before deploying"""
    # local("./manage.py validate_templates")
    local("prospector")


@task
def version():
    """ Show last commit to the deployed repo. """
    with cd(PROJECT_FOLDER):
        run('git log -1')


@task
def ping():
    """
    Prints information about the host.
    Use it to check if env configuration is ok.
    """
    run("uname -a")


@task
def restart():
    """
    Re-starts the webserver that is running the Django instance
    """
    sudo('supervisorctl restart all')


@task
def cs(force_run=True):
    """
    run collectstatic
    Args:
        force_run:

    Returns:

    """
    with cd(PROJECT_FOLDER), prefix(VENV_CMD):
        run("./manage.py collectstatic --noinput")


@task
def migrate(app=''):
    """
    Run the migrations to the database
    Usage: fab migrate:app_name
    """
    with cd(PROJECT_FOLDER), prefix(VENV_CMD):
        run("./manage.py migrate %s --noinput" % app)


@task
def deploy(*skips):
    """
        deploy changes to host by all below tasks
        checks - run any local tests and deployment checks
        push -
        pip - check requirements.txt
        migrate -
        bkp -
        restart -
    """
    green_caption('Deploy project in {}'.format(PROJECT_FOLDER))
    clean()
    push()
    pip()
    cs()
    migrate()
    manage('update_default_mail_templates')
    restart()


@task
def getlog():
    get("/var/log/james/uwsgi.log", './local')


@task
def viewlog():
    run("tailf /var/log/james/uwsgi.log")


def local_sudo():
    from backend.config import CONFIG
    import sys
    sys.path.insert(0, '.')
    from subprocess import Popen, PIPE
    p = Popen(['sudo', '-S', 'true'], stdin=PIPE, stderr=PIPE, universal_newlines=True)
    p.communicate(CONFIG.local_password + '\n')


@task
def start():
    local_sudo()
    local('sudo -S true')
    local('sudo systemctl start mariadb')
    local('yarn dynalite --port 9000')
    # local('sudo systemctl start rabbitmq')


@task
def stop():
    local('sudo systemctl stop mariadb')
    # local('sudo systemctl stop rabbitmq')


@task
def error_uwsgi():
    green_caption('Tail log for uwsgi.')
    sudo('tail /var/log/easydev.err.log')


@task
def ping():
    run('uname -a')


@task
def error_celery():
    # run('celery inspect registered')
    green_caption('download log for celery.')
    get('/var/log/easy_celary.err.log', './.local')


@task
def start_celery():
    run('celery -A backend worker -l info -B')


@task
def error_email():
    green_caption('Tail log for email.')
    with cd(PROJECT_FOLDER):
        sudo('tail logs/email-details.log')


@task
def error_sms():
    green_caption('Tail log for Twilio.')
    with cd(PROJECT_FOLDER):
        sudo('tail logs/twillio.log')


@task
def get_sms_log():
    with cd(PROJECT_FOLDER):
        get('twillio.log', '.')


@task
def manage(cmd):
    """run management commands remotely"""
    with prefix(VENV_CMD), cd(PROJECT_FOLDER):
        run("./manage.py {}".format(cmd))


@task
def test(*apps, tests=True):
    """ Runs the Django test suite as is.  """
    sys.path.insert(0, os.path.abspath('.'))
    from backend.settings.base import PROJECT_LIST
    apps = apps or PROJECT_LIST

    #  -rw -W ignore -W once::DeprecationWarning --> to show only deprecation warning
    local("pytest "
          f"{' '.join([app for app in apps])} "
          f"{'tests' if tests else ''} "

          "-p no:monkeytype "  # disable annontations plugin running

          "-rw "  # -rw -W ignore -W once::DeprecationWarning --> to show only deprecation warning
          "--cov-report term:skip-covered "
          "--cov-report term-missing "
          "--cov-report html "
          f"{''.join([' --cov {}'.format(app) for app in apps])} "
          # "-vvv "
          "--fail-on-template-vars "
          "--doctest-modules "
          # "-s "  # do not capture any stdout
          )


@task
def extra_requirements():
    local('pip-extra-reqs --ignore-file=frontend/* .')


## docker tasks ##
@task
def run_docker():
    import sys
    sys.path.insert(0, '.')
    from backend.config import CONFIG
    local_sudo()
    local('sudo systemctl start docker')
    # local('docker pull lambci/lambda:build-python3.6')
    local(f'sudo docker build -t {PROJECT_NAME} .')
    local(f'docker run -ti '
          f'-e AWS_SECRET_ACCESS_KEY={CONFIG.APP_AWS_SECRET_ACCESS_KEY} '
          f'-e AWS_ACCESS_KEY_ID={CONFIG.APP_AWS_ACCESS_KEY_ID} '
          f'-e AWS_DEFAULT_REGION=us-east-1 '
          f'-v $(pwd):/var/task  --rm {PROJECT_NAME}')


ZAPPA_DIST_DIR = os.path.join(os.path.dirname(__file__), 'dist')


@task
def pew_in(command, env="bf-prod", prefix=''):
    t = time.time()
    local(f"{prefix} pew in {env} {command}")
    print("Time taken: ", time.time() - t, 'seconds')


@task
def clean_dist():
    # cleanup any zip files or previously unpacked ones
    local("find . -name 'bookedfusion-*.zip' -delete")
    print(ZAPPA_DIST_DIR, '---', os.path.exists(ZAPPA_DIST_DIR))
    if os.path.exists(ZAPPA_DIST_DIR):
        shutil.rmtree(ZAPPA_DIST_DIR)


@task
def test_dist(env='staging'):
    """create a package where we can directly test how the lambda function gets invoked"""
    zip_file_name = "`printf '%s' bookedfusion-*.zip`"
    clean_dist()
    # call zappa to create a package
    pew_in(f"pip install -r requirements.txt")
    pew_in(f'zappa package {env}')

    # unzip and remove it
    pew_in(f"unzip -q {zip_file_name} -d {ZAPPA_DIST_DIR}")
    pew_in(f"rm {zip_file_name}")

    # instructions
    print(
        "\n\nInstructions to use test package: ",
        green('cd dist/`'), 'and Use',
        green('RUN_VENV="test_dist" python handler.py'),
        'to test the package.',
    )
    print(magenta('Note: use Python executable without any venv to see that it all dependencies are packages'))


@task
def test_with_docker():
    """create a package where we can directly test how the lambda function gets invoked"""
    test_dist()
    # if you have docker setup then
    # https://github.com/lambci/docker-lambda
    local(f"cd {ZAPPA_DIST_DIR} && "
          f"docker run --rm -v $PWD:/var/task {PROJECT_NAME} handler.lambda_handler")


@task
def zappa_deploy(env: str = "staging", cs=True, lex=False):
    t = time.time()
    clean_dist()
    pew_in(f"pip install -r requirements.txt")
    # local("cp /home/noor/.local/share/virtualenvs/bf/lib/python3.6/site-packages/django_ses/migrations/*
    # /home/noor/.local/share/virtualenvs/bf-prod/lib/python3.6/site-packages/django_ses/migrations/")
    pew_in("python manage.py makemigrations django_ses")
    # collect static files to s3
    if cs:
        pew_in("python manage.py collectstatic  --noinput", prefix=f"RUN_ENV={env}")
    # pew_in("git push")
    pew_in(f"zappa update {env}")
    pew_in(f"zappa manage {env} migrate")
    pew_in(f"zappa manage {env} update_default_settings")
    update_lambda_functions(env)
    if lex:
        update_lex_bot_init_function_settings(env)
    print('Time taken for command zappa_deploy: ', time.time() - t, 'seconds')


@task
def update_lex_bot_init_function_settings(env: str = 'staging'):
    import boto3
    from backend.config import CONFIG

    client = boto3.client('lex-models', aws_access_key_id=CONFIG.APP_AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=CONFIG.APP_AWS_SECRET_ACCESS_KEY,
                          region_name=CONFIG.REGION_NAME, )
    for intent in ['SMSBot', 'CancelAppointmentIntent', 'ForwardNewUserIntent', 'ForwardReturningUser',
                   'RescheduleAppointmentIntent', ]:
        checksum = client.get_intent(name=intent, version='$LATEST')['checksum']
        client.put_intent(
            name=intent, dialogCodeHook={
                'uri': f'arn:aws:lambda:us-east-1:029992932068:function:{PROJECT_NAME}-{env}',
                'messageVersion': '1.0'
            },
            checksum=checksum,
        )


@task
def update_lambda_functions(env: str = 'staging'):
    """to be invoked from Lex Bots"""
    import boto3
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    for cmds in [
        dict(
            StatementId='chatbot-dialog',
            Principal='lex.amazonaws.com',
        ),
        dict(
            StatementId='1',
            Principal='connect.amazonaws.com',
            SourceArn='arn:aws:connect:us-east-1:029992932068:instance/e7f9f1cf-2fc6-4055-bc22-6967ed18fd90',
            SourceAccount='029992932068',
        )
    ]:
        try:
            # add permissions for invoking zappa functions from lex and aws connect
            resp = lambda_client.add_permission(
                FunctionName=f'{PROJECT_NAME}-{env}',
                Action='lambda:InvokeFunction',
                **cmds,
            )
            print(resp)
        except Exception as ex:
            msg = str(ex)
            print(msg)
            # recent boto versions raise exceptions when adding existing permissions
            if f"The statement id ({cmds['StatementId']}) provided already exists" not in msg:
                raise ex


@task
def zappa_tail(env='staging'):
    local('rm -f -- tailed.log')
    local(f"zappa tail {env} | grep --line-buffered '' | tee -a tailed.log")


@task
def awslogs_tail(env='staging'):
    """faster version"""
    local('rm -f -- tailed.log')
    local(f"awslogs get /aws/lambda/{PROJECT_NAME}-{env} -w | grep --line-buffered '' | tee -a tailed.log")
