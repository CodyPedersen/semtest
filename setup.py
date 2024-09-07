"""PyPi vizrecurse setup"""
# pylint: disable=import-error
from pathlib import Path

from setuptools import setup, find_packages

setup(
    name='semtest',
    version='0.0.0',
    author='Cody Pedersen',
    description='LLM semantic testing and benchmarking framework',
    long_description=(Path(__file__).parent/"README.md").read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    py_modules=['semtest'],
    entry_points={
        'console_scripts': [
            'semtest=semtest:semantic_test_runner',
        ],
    },
    classifiers=[
    'Programming Language :: Python :: 3.12',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research'
    ],
    python_requires='>=3.12',
    readme="README.md",
    install_requires=[],
    package_data={'semtest': ['py.typed']},
)
