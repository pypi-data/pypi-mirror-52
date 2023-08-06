# HBRS Grader

[![pipeline status](https://gitlab.com/joergbrech/hbrs_grader/badges/master/pipeline.svg)](https://gitlab.com/joergbrech/hbrs_grader/commits/master)

**A Jupyter Notebook workflow for grading exams at the Hochschule Bonn-Rhein-Sieg**

This workflow allows you to
 - import a csv-file (e.g. obtained from DIAS), 
 - enter points for each student for an exam consisting of a specified of assignments, 
 - decide on a passing grade and the limit of a *"perfect"* grade and 
 - create publishable results with some additional exam statistics generated using pandas.

Check out [this example notebook](hbrs_grader/template/template.ipynb). The [exported HTML-document](https://gitlab.com/joergbrech/hbrs_grader/-/jobs/artifacts/master/download?job=template) will not contain the code cells. Since the export format is HTML and most online teaching tools such as MOODLE or ILIAS support HTML, you can simply copy the HTML source to a text node of your online course.

## Installation

Run 

```bash
python setup.py install 
```

from the root diretory of this repository.

## Usage

### Create a Notebook from template

Run 

```bash
hbrs-grader create 2019_MyExam
```

to create a Jupyter notebook called `2010_MyExam.ipynb` in your current working directory. Execute it using `jupyter-notebook` or `jupyter-lab`:

```bash
jupyter-notebook ./2019_MyExam.ipynb`
```

### Grade your exam

Then just follow the instructions in the code comments. You can add additional code cells if you like, just make sure that all code cells contain the following metadata

```json
{
    "hideCode": true,
    "hidePrompt": true
}
```

so that they don't show up in the published html.

### Publish the results

Once you are done grading, you can export the notebook to HTML with the following command:

```bash
hbrs-grader export-notebook 2019_MyExam.ipynb
```
