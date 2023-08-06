from setuptools import setup

setup(
    name='furs_fiscalization',
    packages=['furs_fiscalization'],
    version='0.1.0',
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Python library for simplified communication with FURS (Financna uprava Republike Slovenije).',
    author='Hermes d.o.o.',
    author_email='info@hermes-solutions.si ',
    url='https://github.com/HermesGH/furs-fiscalization',
    download_url = 'https://github.com/HermesGH/furs-fiscalization/archive/v_01.tar.gz',
    keywords=['FURS', 'fiscal', 'fiscal register', 'davcne blagajne'],
    classifiers=[],
    package_data={'furs_fiscalization': ['certs/*.pem']},
    install_requires=[
        'pytz>=2017.2',
        'requests>=2.20.0',
        'python-jose==3.0.1',
        'pyOpenSSL>=17.5.0',
    ]
)
