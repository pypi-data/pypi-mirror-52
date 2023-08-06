import setuptools

setuptools.setup(
    name="kabocha",
    version="1.0.1",
    description="JSON error extension to tastypie ",
    long_description="Extension to django-tastypie to help deal with more errors directly with JSON",
    keywords="django, tastypie, json, errors, api, rest",
    author="Josh Stegmaier <jrs@joshstegmaier.com>",
    author_email="jrs@joshstegmaier.com",
    url="https://github.com/JoshStegmaier/kabocha/",
    license="MIT",
    packages=["kabocha", "kabocha.errors"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)