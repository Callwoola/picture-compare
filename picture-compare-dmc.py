#coding:utf-8

from fabric.api import run
from fabric.tasks import execute
# from fabric.api import env
from fabric.api import run, env, sudo, put, shell_env, prompt
from fabric.colors import red, green


local_path = "/Users/liyang/Code/picture-compare"
dev_engine_path = "/opt/lampp/htdocs/dmc/engine"
alis1_engine_path = "/opt/lampp/htdocs/dmc-alis1/engine"


def dev_run_script():
    envs = [
        {
            'path':"/mountapp/picture-compare-alis1",
            'port':"5556",    
        },
        {
            'path':"/mountapp/picture-compare",
            'port':"5555",
        },
    ]
    for deploy in  envs:
        deploy_path = deploy['path']
        deploy_port = deploy['port']

        clear_src = "rm -rf "+ deploy_path + "/src"
        print clear_src

        run(clear_src)

        put(local_path + "/src", deploy_path + "/")
        put(local_path + "/server.py", deploy_path + "/server.py")
        put(local_path + "/config.yaml", deploy_path + "/config.yaml")

        run("sed -i -e 's/5555/" + deploy_port +"/g' " + deploy_path + "/config.yaml")
        run("sed -i -e 's/5555/" + deploy_port +"/g' " + deploy_path + "/server.py")
        
        run('mkdir -p '+ deploy_path +'/img/imgdb')
        run('mkdir -p '+ deploy_path +'/img/tmp')
        run('mkdir -p '+ deploy_path +'/img/storage')
        run('chmod -R 777 '+ deploy_path +'/*')
        
    run("sudo service supervisor restart")

def prod_deploy():
    deploy_path = "/mnt/picture-compare"
    # run('ls /mnt')
    # run('mkdir '+ deploy_path)
    put(local_path + "/src", deploy_path + "/")
    put(local_path + "/server.py", deploy_path + "/server.py")
    put(local_path + "/config.yaml", deploy_path + "/config.yaml")

    #run("sed -i -e 's/5555/" + deploy_port +"/g' " + deploy_path + "/config.yaml")
    #run("sed -i -e 's/5555/" + deploy_port +"/g' " + deploy_path + "/server.py")

    run('mkdir -p '+ deploy_path +'/img/imgdb')
    run('mkdir -p '+ deploy_path +'/img/tmp')
    run('mkdir -p '+ deploy_path +'/img/storage')
    run('chmod -R 777 '+ deploy_path +'/*')

def run_index_image_dev():
    run('cd ' + dev_engine_path + ' && php artisan index:image --env=dev')

def run_index_image_alis1():
    run('cd ' + alis1_engine_path + ' && php artisan index:image --env=alis1')

print red('start >>>>>')
print u"\U0001F680"
print u"\U0001F31E"
environment = prompt(
    green('Please choose you task:') + \
    red(
        '\n 1 > (dev, alis1) dmc-picture-compare '+ \
        '\n 2 > (dev) index dev image ' + \
        '\n 3 > prod picture-compare deploy ' + \
        '\n 4 > (dev) index alis1 image ' + \
        '\n'
    ) + \
    green('-:'),
    key='nice',
    validate=int
)

if environment == 1:
    env.password = 'Gzdmc2015'
    env.hosts = ['root@dcp.dev.gzdmc.net']
    env.passwords = {'root@dcp.dev.gzdmc.net': 'Gzdmc2015'}
    # env.shell = "/bin/sh -c"
    #  run('cd /opt/apps/myblog && sudo kill -9 $(ps -aux|grep "python server.py"|awk "{print $2}") || true')
    execute(dev_run_script)
if environment == 2:
    env.password = 'Gzdmc2015'
    env.hosts = ['root@dcp.dev.gzdmc.net']
    env.passwords = {'root@dcp.dev.gzdmc.net': 'Gzdmc2015'}
    # env.shell = "/bin/sh -c"
    execute(run_index_image_dev)
if environment == 3:
    env.password = 'Gzdmc2015'
    env.hosts = ['root@dcp.gzdmc.net']
    env.passwords = {'root@dcp.gzdmc.net': 'Gzdmc2015'}
    env.port = 50000
    execute(prod_deploy)
if environment == 4:
    env.password = 'Gzdmc2015'
    env.hosts = ['root@dcp.dev.gzdmc.net']
    env.passwords = {'root@dcp.dev.gzdmc.net': 'Gzdmc2015'}
    execute(run_index_image_alis1)
