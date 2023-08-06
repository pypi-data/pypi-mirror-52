from setuptools import setup, find_packages

setup(
    name='hbrs_grader',
    version='1.0.1',
    packages=find_packages(),
    package_data={'': ['template.ipynb', 'exam_in.csv']},
    license='MIT',
    author='Jan Kleinert',
    author_email='Jan.Kleinert@h-brs.de',
    description='A jupyter workflow for grading exams',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="http://gitlab.com/joergbrech/hbrs_grader",
    download_url="https://gitlab.com/joergbrech/hbrs_grader/-/archive/v1.0.1/hbrs_grader-v1.0.1.tar.gz",
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "jupyter",
        "IPython",
        "nbformat",
        "nbconvert",
        "hide_code",
        "click",
        "importlib_resources ; python_version<'3.7'"
    ],
    entry_points={
        'console_scripts': ['hbrs-grader = hbrs_grader.core:cli']
    }
)