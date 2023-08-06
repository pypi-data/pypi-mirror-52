from setuptools import setup

# read the contents of your README file
def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name='sort_pckg_frarg',
    version='0.1',
    description='sorting algorithms',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='algorithm sort wonderful',
    license='MIT',
    packages=['sort'],
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    zip_safe=False
)
