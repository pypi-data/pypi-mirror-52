from setuptools import setup, find_packages

setup(
    name='google_oauth2_desktop_flow',
    version='0.0.7',
    author='Paulo Rosário',
    author_email='paulo.filip3@gmail.com',
    packages=find_packages(),
    install_requires=[
        'flask',
        'google-auth-oauthlib',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'google-oauth-tokens = google_oauth2_desktop_flow.cli:main'
        ]
    }
)
