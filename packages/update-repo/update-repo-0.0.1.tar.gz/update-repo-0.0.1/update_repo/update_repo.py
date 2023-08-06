def update_repo(url='https://github.com/ffreemt/update-repo.git'):
    ''' git clone/pull git repo
    >>> update_repo(repo_https_git_address)
    '''
    import os, sys, shlex
    import subprocess as sp
    from os import chdir
    from pathlib import Path

    dirname = Path(url).stem
    chdir('/content')
    if not Path('data').exists():
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
    else:
        chdir(dirname)
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
    chdir('/content/%s' % dirname)
    print(' Now in /content/%s\n' % dirname)
