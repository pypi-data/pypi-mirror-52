from distutils.core import setup


setup(
    name='mocker_client',
    version='0.0.1dev1',
    description='client for http mocker server https://github.com/vilus/mocker',
    packages=['mocker_client'],
    author='Shevchenko Vladimir',
    url='https://github.com/vilus/mocker_client',
    install_requires=['requests']
)
