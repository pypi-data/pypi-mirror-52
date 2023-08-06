from setuptools import setup, find_packages

setup(
    name = "django-shopify-abandoned-checkout",
    version = "0.0.4",
    author = "David Burke",
    author_email = "dburke@thelabnyc.com",
    description = ("Send Shopify abandoned checkout emails from Django"),
    license = "Apache License",
    keywords = "django shopify",
    url = "https://gitlab.com/thelabnyc/django-shopify-abandoned-checkout",
    packages=find_packages(exclude=('sandbox.*', 'sandbox',)),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=[
        'ShopifyAPI>=5.0.0'
    ]
)
