# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.en.md", "r") as fh:
    long_description = fh.read()

setup(
    name="yandex_checkout",
    version="1.4.0",
    description="Yandex Checkout SDK Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yandex-money/yandex-checkout-sdk-python",
    author="Yandex.Money",
    packages=["yandex_checkout", "yandex_checkout.domain.request", "yandex_checkout.domain.response",
              "yandex_checkout.domain.notification", "yandex_checkout.domain.models", "yandex_checkout.domain",
              "yandex_checkout.domain.models.confirmation", "yandex_checkout.domain.models.confirmation.request",
              "yandex_checkout.domain.models.confirmation.response", "yandex_checkout.domain.models.payment_data",
              "yandex_checkout.domain.models.payment_data.request", "yandex_checkout.domain.common",
              "yandex_checkout.domain.models.payment_data.response", "yandex_checkout.domain.exceptions"],
    install_requires=["requests", "uuid", "urllib3"],
    zip_safe=False,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
