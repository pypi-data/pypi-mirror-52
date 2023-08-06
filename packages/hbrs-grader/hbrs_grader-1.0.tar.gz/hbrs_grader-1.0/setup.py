from setuptools import setup, find_packages

setup(
    name='hbrs_grader',
    version='1.0',
    packages=find_packages(),
    package_data={'': ['template.ipynb', 'exam_in.csv']},
    license='To Do',
    author='Jan Kleinert',
    author_email='Jan.Kleinert@h-brs.de',
    description='A jupyter workflow for grading exams',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'jupyter',
        'IPython',
        'nbformat',
        'nbconvert',
        'hide_code',
        'click'
    ],
    entry_points={
        'console_scripts': ['hbrs-grader = hbrs_grader.core:cli']
    }
)