from setuptools import setup, find_packages

with open('VERSION.txt', 'r') as version_file:
    version = version_file.read().strip()

# requires = ['numpy==1.14.0', 'pandas==0.19.2', 'pysam==0.10.0', 'HTSeq==0.9.1']
requires = ['numpy==1.16.4', 'pysam==0.15.2']

setup(
    name='bbcu.bt-flor',
    version=version,
    author='Refael Kohen',
    author_email='refael.kohen@gmail.com, refael.kohen@weizmann.ac.il',
    packages=find_packages(),
    scripts=[
        'scripts/bt-flor.py',
        'scripts/bt-flor-separate-bam-strands.py',
        'scripts/fetch-bam.py',
    ],
    description='BT-FLOR - Build Transcripts From LOng-Reads',
    long_description=open('README.md').read(),
    long_description_content_type='text/x-rst',
    install_requires=requires,
    tests_require=requires + ['nose'],
    include_package_data=True,
    test_suite='nose.collector',
)

