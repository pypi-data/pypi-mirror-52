'''
clone/pull a repo to destdir

default repo: https://github.com/ffreemt/update-repo.git
default destdir: '/content' for colab or ~ or HOME if '/content' does not exist

'''

from os import chdir
from pathlib import Path
import shlex
import subprocess as sp

THISREPO = 'https://github.com/ffreemt/update-repo.git'


def update_repo(url=THISREPO, destdir='/content'):
    ''' git clone/pull git repo
    >>> update_repo(repo_https_git_address)
    '''

    if Path(destdir).exists():
        chdir(destdir)
    else:
        chdir(Path().home())
        
    repo_dirname = Path(url).stem
    
    if Path(repo_dirname).exists():
        chdir(repo_dirname)
        print('git pull %s...' % url)
        # os.system('git pull')
        proc = sp.Popen(
            shlex.split('git pull %s' % url),
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        out, err = proc.communicate()
        if err:
            print('>> %s' % err.decode())
        print('git pull ...%s' % out.decode())
    else:
        print('git clone %s...' % url)
        # os.system('git clone %s' % url)
        proc = sp.Popen(
            shlex.split('git clone %s' % url),
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        out, err = proc.communicate()
        if err:
            print('>> %s, %s' % (err.decode(), out.decode()))
        else:
            print('git clone...%s' % out.decode())

    chdir('%s/%s' % repo_dirname)
    print(' Now in %s/%s\n' % (destdir, repo_dirname))
