import setuptools

setuptools.setup(
    name='runcible',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Grayson Head',
    author_email='grayson@graysonhead.net',
    url='https://github.com/graysonhead/runcible',
    packages=setuptools.find_packages(),
    license='GPL V3',
    install_requires=[
        'paramiko>=2.4.2',
        'colorama>=0.4.1',
        'cryptography==2.4.2',
        'pyyaml>=5.1',
        'mergedb>=0.0.11',
        'pyserial>=3.4'
    ],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': [
            'runcible = runcible.__main__:main'
        ]
    }
)
