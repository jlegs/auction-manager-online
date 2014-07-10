from fabric.api import local, run, env, abort


env.hosts = ['ec2-54-82-112-202.compute-1.amazonaws.com']
env.user = 'wildlife'
env.forward_agent = True

def test():
    local('./manage.py test')


def remote_in():
    local('ssh wildlife@ec2-54-82-112-202.compute-1.amazonaws.com')

def django_shell():
    '''
    Enters the django shell on the server for debugging or testing
    '''
    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && ./manage.py shell_plus')


def gunicorn(arg):
    '''
    gunicorn command. inserts any arguments you send with it to the supervisorctl command. run this after ""fab deploy_code""
    e.g.: fab gunicorn:restart == supervisorctl restart wildlife
    '''
    if arg in ['start', 'stop', 'restart', 'reload', 'reread']:
        run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && supervisorctl %s wildlife' % arg)
    else:
        abort('Not a valid gunicorn command.')


def deploy_code():
    '''
    Pulls the latest version of the codebase to the server
    '''
    run('cd website/auction-manager-online && git pull')

def install_dependencies():
    '''
    runs pip install -r requirements.txt to install the dependencies.
    '''
    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && pip install -r requirements.txt')



def full_deploy():
    '''
    Gets latest code on the server, installs dependencies and restarts gunicorn for the changes to take effect.
    '''
    run('cd website/auction-manager-online && git pull')

    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && pip install -r requirements.txt')

    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && ./manage.py migrate')

    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && ./manage.py collectstatic')

    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && supervisorctl restart wildlife')


def nginx(arg):
    '''
    Runs an nginx command
    '''
    if arg in ['start', 'stop', 'restart', 'reload', 'reread']:
        run('sudo service nginx %s' % arg)
    else:
        abort('Not a valid nginx command.')


