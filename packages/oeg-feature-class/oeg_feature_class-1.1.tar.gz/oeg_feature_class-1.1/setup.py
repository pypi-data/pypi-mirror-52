import setuptools


long_description = """
# oeg_feature_class

Module for anomaly dimension classification for intelligent pig inspection of pipelines
"""

setuptools.setup(
    name = 'oeg_feature_class',
    version = '1.1',
    author = 'Vitaly Bogomolov',
    author_email = 'mail@vitaly-bogomolov.ru',
    description = 'Module for anomaly dimension classification',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/vb64/oeg.feature.class',
    packages = ['oeg_feature_class'],
    download_url = 'https://github.com/vb64/oeg.feature.class/archive/v1.1.tar.gz',
    keywords = ['python', 'OrgEnergoGaz', 'anomaly', 'pipelines', 'MFL', 'TFI'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
