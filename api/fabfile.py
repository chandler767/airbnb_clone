from fabric.api import *
from fabric.operations import *

dist = "airbnb_clone"
env.roledefs = {
	'deploy_chandler': ['ubuntu@54.183.231.35'],
	'deploy_josh': ['ubuntu@54.183.231.35']
}

@roles('deploy_chandler')
def deploy_chandler():
	''' cd into webserver root '''
	with cd('/usr/share/nginx'):
		''' Remove old '''
		with settings(warn_only=True):
			run("sudo rm -rf html")
		''' clone repo '''
		run('sudo rm -rf html; sudo git clone https://github.com/jdeepee/airbnb_clone.git html')

@roles('deploy_josh')
def deploy_josh():
	''' cd into webserver root '''
	with cd('/usr/share/nginx'):
		''' Remove old '''
		with settings(warn_only=True):
			run("sudo rm -rf html")
		''' clone repo '''
		run('sudo rm -rf html; sudo git clone https://github.com/jdeepee/airbnb_clone.git html')

def install_requirements():
    """ Install required packages. """
    sudo('apt-get update')
    sudo('apt-get install -y python')
    sudo('apt-get install -y python-pip')
    sudo('apt-get install -y python-virtualenv')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y gunicorn')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y git')