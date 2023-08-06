from setuptools import setup

setup(
    name='rabbit-clients',
    version='0.9.0',
    packages=['tests', 'rabbit_clients', 'rabbit_clients.clients'],
    url='',
    license='MIT License',
    author='Aaron Burgess',
    author_email='geoburge@gmail.com',
    description='Provides decorators for basic RabbitMQ support with respect to publishing and consuming messages.',
    install_requires=[
        'pika'
    ],
    extra_require=[
        'pytest',
        'pylint'
        'coverage',
        'pytest-cov'
    ]
)
