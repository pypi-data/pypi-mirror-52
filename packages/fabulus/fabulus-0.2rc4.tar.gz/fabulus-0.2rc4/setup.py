import setuptools

VERSION = '0.2rc4'

setuptools.setup(
    name='fabulus',
    version=VERSION,
    author='Stefan B, Alexander R',
    author_email='Steve2608@users.noreply.github.com',
    url='https://github.com/AlexRaschl/FABULUS-A-machine-learning-enterprise',
    download_url='https://github.com/AlexRaschl/FABULUS-A-machine-learning-enterprise/archive/'
                 f'v_{VERSION}.tar.gz',
    description='Utility packages for Machine Learning and Data Visualisation',
    packages=[
        'fabulus',
        'fabulus/_internal',
        'fabulus/io',
        'fabulus/net',
        'fabulus/postprocessing',
        'fabulus/unsup',
        'fabulus/vis',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'matplotlib',
        'numpy',
        'sklearn',
        'tensorflow'
    ]
)
