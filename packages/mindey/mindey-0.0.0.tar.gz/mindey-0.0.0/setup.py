from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='mindey',
    version='0.0.0',
    description='Shares my contact info.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/mindey',
    author='Mindey',
    author_email='mindey@qq.com',
    license='UNDEFINED',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)

