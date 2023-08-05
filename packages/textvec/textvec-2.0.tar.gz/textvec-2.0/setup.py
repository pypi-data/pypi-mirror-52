from setuptools import setup, find_packages


setup(
    name='textvec',
    use_scm_version=True,
    description='Supervised text features extraction',
    version='2.0',
    url='https://github.com/zveryansky/textvec',
    author='Alex Zveryansky',
    author_email='',
    license='MIT',
    classifiers=[
    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
    ],
    keywords='text nlp vectorization scikit-learn',
    packages=find_packages(exclude=['examples']),
    install_requires=['scikit-learn', 'numpy', 'scipy', 'gensim'],
)
