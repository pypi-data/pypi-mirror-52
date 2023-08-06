import setuptools

setuptools.setup(
    name='ucloud_common',
    version='0.5.4',
    description='Common Code shared by most of ucloud projects',
    url='https://code.ungleich.ch/ucloud/ucloud_common',
    author='ungleich',
    author_email='hacking@ungleich.ch',
    packages=setuptools.find_packages(),
    install_requires=[
        'etcd3-wrapper',
        'python-decouple'
        ],
    classifiers=[
        'Programming Language :: Python :: 3',
        ],
    python_requires='>=3.5',
)
