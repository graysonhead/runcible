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
        'cryptography>=2.5.0',
        'pyyaml>=5.1',
        'mergedb>=0.1.0',
        'pyserial>=3.4'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Repository': 'https://github.com/graysonhead/runcible',
        'Documentation': 'https://runcible.readthedocs.io/en/latest/index.html',
        'Gitter': 'https://gitter.im/runcible_project/community'
    },
    python_requires='>=3.5, <4',
    entry_points={
        'console_scripts': [
            'runcible = runcible.__main__:main'
        ]
    }
)
