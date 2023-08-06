import setuptools

from os.path import dirname, join

with open(join(dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nf-batch-runner",
    version="0.0.9",
    author="Centre for Genomic Pathogen Surveillance",
    author_email="cgps@sanger.ac.uk",
    description="Installs nf-batch-runner in your AWS account",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cgps/nf-batch-runner",
    packages=setuptools.find_packages(),
    py_modules=['nf-batch-runner'],
    entry_points='''
        [console_scripts]
        nf-batch-runner=nf_batch_runner.cli:cli
    ''',    
    install_requires=[
      "boto3>=1.9.227",
      "bcrypt>=3.1.7",
      "Click>=7.0",
      "PyYAML>=5.1.2"
    ],
    classifiers=[
      "Development Status :: 4 - Beta",
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent",
    ],
    keywords="aws batch nextflow bioinformatics pipeline",
    project_urls={
      'Source': 'https://gitlab.com/cgps/nf-batch-runner/',
    },
    python_requires='>=3',
)
