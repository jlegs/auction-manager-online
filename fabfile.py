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
    gunicorn command. inserts any arguments you send with it to the supervisorctl command.
    e.g.: fab gunicorn:restart == supervisorctl restart wildlife
    '''
    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && supervisorctl %s wildlife' % arg)


def deploy_code():
    run('cd website/auction-manager-online && git pull')

def install_dependencies():
    run('cd website/auction-manager-online && source ../../.virtualenvs/wildlife/bin/activate && pip install -r requirements.txt')



