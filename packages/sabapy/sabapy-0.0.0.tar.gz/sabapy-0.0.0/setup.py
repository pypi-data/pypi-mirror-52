from setuptools import setup

setup(
    name='sabapy',
    version='0.0.0',
    description='Misc functions used during my work',
    long_description='',
    url='',
    author='Nikolay Dudaev',
    author_email='nikolay.dudaev@icloud.com',
    license='MIT',
    packages=[
        'sabapy',
    ],
    zip_safe=False,
    install_requires=[
        'numpy',
        'pandas'
    ],
    include_package_metadata=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    # entry_points = {
    #     'console_scripts': [
    #         'collect_data=tracking_service.collect_data:collect_data',
    #         ],
    # }
)
