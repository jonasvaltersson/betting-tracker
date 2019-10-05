import subprocess


def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

def get():
    git_commit = get_git_revision_short_hash()
    
    return dict(
        version=f'commit_{git_commit}'
    )