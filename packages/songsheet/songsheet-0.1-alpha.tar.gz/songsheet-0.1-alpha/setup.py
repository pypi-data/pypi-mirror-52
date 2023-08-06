from distutils.core import setup

# setup(
#     name='Songsheet',
#     version='0.1dev',
#     packages=['songsheet',],
#     license='GNU GENERAL PUBLIC LICENSE',
#     long_description=open('README.md').read(),
# )

from distutils.core import setup
setup(
    name='songsheet',
    packages=['songsheet'],   # Chose the same as "name"
    version='0.1-alpha',
    license='MIT',
    description='Parses songsheet strings',
    author='Aaron Cohen',
    author_email='aaroncohendev@gmail.com',
    url='https://github.com/kahunacohen/songsheet',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['music', 'lyrics'],
    install_requires=[
        'validators',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
