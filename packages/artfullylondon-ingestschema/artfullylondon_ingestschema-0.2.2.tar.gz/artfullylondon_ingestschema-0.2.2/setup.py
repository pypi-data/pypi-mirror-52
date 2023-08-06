from setuptools import setup


setup(
    name='artfullylondon_ingestschema',

    version='0.2.2',
    python_requires='>=3.7',

    description='',
    long_description='',

    author='Steve Johns',
    author_email='steve@stevejay.net',

    license='MIT License',

    packages=['artfullylondon.ingestschema'],
    zip_safe=False,

    package_data={
        'artfullylondon.ingestschema': ['*.json'],
    },
)
