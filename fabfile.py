from fabric.api import local

def backup():
    local('git pull origin master')
    local('git add -A')
    
    print("enter your commit comments:")
    comment = raw_input()
    local('git commit -m "%s"' % comment)
    
    local('git push origin master')
    
def deploy():
    local('pip freeze > requirements.txt')
    local('git pull heroku master')
    local('git add -A')
    
    print("enter your commit comments:")
    comment = raw_input()
    local("git commit -m '%s'" % comment)
    
    # local('git push')
    
    local('./manage.py collectstatic')
    
    # local('heroku maintenance:on')
    
    local('git push heroku master')

    local('heroku run ./manage.py makemigrations')
    local('heroku run ./manage.py migrate')
    
    # local('heroku maintenance:off')
    
    local('heroku restart')