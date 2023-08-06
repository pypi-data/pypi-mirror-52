from setuptools import setup
setup(
    name='rocket-launcher',
    version='0.2.3.1',
    author='who',
    author_email='who@whooami.me',
    scripts=[
        'rocket-launcher',
        'rockets/bin/configure-file-browser',
        'rockets/bin/configure-multiplexer',
        'rockets/bin/configure-version-controller',
        'rockets/bin/configure-secure_shell',
        'rockets/bin/set-terminal-fish',
        'rockets/bin/set-text-editor',
    ],
    packages=['rockets'],
)
