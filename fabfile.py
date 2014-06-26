from fabric.api import local, run, env


env.hosts = ['ec2-54-82-112-202.compute-1.amazonaws.com']
env.user = 'wildlife'
env.forward_agent = True

def test():
    local('./manage.py test')


def remote_in():
    local('ssh wildlife@ec2-54-82-112-202.compute-1.amazonaws.com')


def gunicorn(arg):
    '''
    gunicorn command. inserts any arguments you send with it to the supervisorctl command. run this after ""fab deploy_code""
    e.g.: fab gunicorn:restart == supervisorctl restart wildlife
    '''
    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && supervisorctl %s wildlife' % arg)


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

    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && supervisorctl restart wildlife')

