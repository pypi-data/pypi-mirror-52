from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='sorting_anton',
    version='0.2',
    description='This package lets you sort lists using Bubble Sort, Quick Sort, Insertion Sort and Selection Sort',
    license='MIT',
    packages=['sorting_anton'],
    keywords='sorting_anton quick insert bubble selection',
    author='Anton Benet',
    author_email='abenet@rbi.com',
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    test_require=['nose'],
    long_description=readme()
)
