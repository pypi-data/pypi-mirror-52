from distutils.core import setup

try:
    with open('README.md') as f:
        readme_text = f.read()
except:
    readme_text = ""
    
setup(
    name = 'lcs_client',
    packages = ['lcs_client'],
    description = 'a python client for interacting with the hackru backend',
    long_description = readme_text,
    version = '1.3',
    license = '',
    author = 'author',
    author_email = 'rnd@hackru.org',
    url = 'https://github.com/HackRU/python-lcs-client',
    install_requires = ['requests'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
)
