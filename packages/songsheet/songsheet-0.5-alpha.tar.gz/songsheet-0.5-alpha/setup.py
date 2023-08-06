from distutils.core import setup


ld = None
with open('./README.md') as f:
    ld = f.read()

setup(
    name='songsheet',
    packages=['songsheet'],   # Chose the same as "name"
    version='0.5-alpha',
    license='MIT',
    description='Parses songsheet strings',
    long_description=ld,
    long_description_content_type="text/markdown",
    author='Aaron Cohen',
    author_email='aaroncohendev@gmail.com',
    url='https://github.com/kahunacohen/songsheet',
    download_url='https://github.com/user/reponame/archive/v_05.tar.gz',
    keywords=['music', 'lyrics'],
    install_requires=[
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
