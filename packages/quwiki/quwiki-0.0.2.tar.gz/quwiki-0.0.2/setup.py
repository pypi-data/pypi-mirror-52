from setuptools import setup


setup(name='quwiki',
      version='0.0.2',
      description='Configurable, extendable and minimalistic wiki for your team generated from multiple sources, e.g. Google Drive, Github and many more.',
      platforms=['noarch'],
      license='Apache',
      packages=[
          'quwiki',
          'quwiki.sources',
          'quwiki.templates',
          'quwiki.templates.light',
      ],
      install_requires=[
          'google-api-python-client',
          'google-auth-httplib2',
          'google-auth-oauthlib',
          'pyyaml',
          'gitpython',
          'markdown',
          'beautifulsoup4',
          'python-slugify',
          'jinja2',
      ],
      scripts=[
          'bin/quwiki',
      ]
      )
