# # -*- coding: iso-8859-1 -*-

import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator

import io
import os
import click

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
from . import template

from IPython.display import display, HTML

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from hide_code import HideCodeHTMLExporter, HideCodePDFExporter


class Exam:

    # grades is a Pandas dataframe that contains the grades of every person
    grades = None

    # the number of assignments in the exam
    prefix = ''
    numParts = 0
    pointsTotal = 0
    pointsPerAssignment = []
    
    gradeDict = {'5,0': 5.0,
                 '4,0': 4,
                 '3,7': 3.7,
                 '3,3': 3.3,
                 '3,0': 3,
                 '2,7': 2.7,
                 '2,3': 2.3,
                 '2,0': 2,
                 '1,7': 1.7,
                 '1,3': 1.3,
                 '1,0': 1,
                 'ne': np.NaN}

    def __init__(self, csvPath, sep='\t', graded=False):

        # open the csv file exported from Dias
        if isinstance(csvPath, list):
            self.grades = pd.read_csv(csvPath[0], sep)
            for idx in range(1, len(csvPath)):
                self.grades = self.grades.append(pd.read_csv(csvPath[idx], sep), ignore_index=True)
        else:
            self.grades = pd.read_csv(csvPath, sep)

        # fill points column with nans, if it isn't already. This criterium is used to find not graded students.
        if not graded:
            self.grades['Punkte'] = np.NAN
            self.grades['Note'] = 'ToDo'
        else:
            inv_grade_dict = {v: k for k, v in self.gradeDict.items()}
            self.grades['Note'] = self.grades['Note'].replace(inv_grade_dict)

        # empty values are often replaced by NaNs, for instance in the "Bemerkung intern", "Bemerkung Aushang" columns.
        # Replace all the NaNs in these columns with empty strings.
        if 'Bemerkung intern' in self.grades:
            self.grades['Bemerkung intern'].fillna('', inplace=True)
        if 'Bemerkung Aushang' in self.grades:
            self.grades['Bemerkung Aushang'].fillna('', inplace=True)

    def setAssignments(self, numAssignments, points, prefix = ''):

        if not len(points) == numAssignments:
            raise IndexError('The list of points does not match the number of assignments')

        self.pointsPerAssignment = points
        self.pointsTotal = sum(points)
        self.numParts = numAssignments
        self.prefix = prefix

        for i in range(1, self.numParts + 1):
            columnName = self.prefix + str(i)

    def enterPoints(self, matrNr, points):

        if not len(points) == self.numParts:
            raise IndexError('The list of points does not match the number of assignments')

        for i in range(0,self.numParts):

            if points[i]< 0 or points[i] > self.pointsPerAssignment[i]:
                raise ValueError('The number of points for assignment {} must be between 0 and {}.'.format(i,self.pointsPerAssignment[i]))

            self.grades.loc[ self.grades['MatrNr'] == matrNr, self.prefix+str(i+1)] = points[i]

        self.grades.loc[ self.grades['MatrNr'] == matrNr, 'Punkte'] = sum(points)

    def Get(self, matrNr):
        return self.grades[ self.grades['MatrNr'] == matrNr ]

    def GetUngraded(self):
        return self.grades[ pd.isnull(self.grades['Punkte']) ]

    def enterColumn(self, matrNr, key, value, append = False):
        if append:
            self.grades.loc[self.grades['MatrNr'] == matrNr, key] += ' ' + value
        else:
            self.grades.loc[self.grades['MatrNr'] == matrNr, key] = value

    def setNE(self, matrNr):
        self.grades.loc[self.grades['MatrNr'] == matrNr, 'Punkte'] = 0
        self.grades.loc[self.grades['MatrNr'] == matrNr, 'Note'] = 'ne'

    def calcGradeBins(self, limitPass, limitPerfect):
        bins = [0]
        for i in range(0, 10):
            bins.append(limitPass * self.pointsTotal + i * (limitPerfect - limitPass) * self.pointsTotal / 9)
        bins.append(self.pointsTotal)
        labels = ['5,0', '4,0', '3,7', '3,3', '3,0', '2,7', '2,3', '2,0', '1,7', '1,3', '1,0']
        return labels, bins

    def calcGrades(self, limitPass, limitPerfect):
        self.limitPass = limitPass
        self.limitPerfect = limitPerfect
        labels, bins = self.calcGradeBins(limitPass, limitPerfect)

        # only edit those students who were there, not the ones with 'ne'
        writers = (self.grades['Note'] != 'ne')
        self.grades.loc[writers, 'Note'] = \
            pd.cut(self.grades[writers]['Punkte'], bins=bins, labels=labels, right=False)

    def gradePointTable(self):
        labels, bins = self.calcGradeBins(self.limitPass,self.limitPerfect)
        A = np.array([bins[:-1]])
        B = np.array([bins[1:]])

        #ceil to nearest half point
        A = np.ceil(A * 2) / 2
        B = np.ceil(B * 2) / 2

        C = np.concatenate((A.T, B.T), axis = 1)
        cols = pd.MultiIndex.from_product([['Punkte'],['>=','<']])
        return pd.DataFrame(data = C, index = labels, columns = cols)

    def assignmentStatistics(self):
        writers = self.grades['Note'] != 'ne'
        columns = []
        for i in range(1, self.numParts+1):
            columns.append(self.prefix + str(i))
        columns.append('Punkte')
        stats = self.grades[writers][columns]

        points = self.pointsPerAssignment[:]
        points.append(self.pointsTotal)

        #calculate discrimination index
        #TODO: KR 20 reliability?
        sorted = stats.sort_values(by='Punkte')
        numWriters = writers.sum()
        twentysevenpercent = int(np.round(0.27 * numWriters))
        lowest = sorted.iloc[:twentysevenpercent]
        highest = sorted.iloc[-twentysevenpercent:]
        discrimination = ((highest.mean() - lowest.mean()) / points).values

        stats = stats.describe()

        stats.loc['Erreichbare Punkte'] = points
        stats.loc['Schwierigkeit'] = stats.loc['mean']/points
        stats.loc['Diskriminierungsindex'] = discrimination

        stats = stats.rename({'mean': 'Mittelwert', 'std': 'Standardabweichung', '25%': '25%-Quantil',
                              '50%' : '50%-Quantil (Median)', '75%' : '75%-Quantil', 'min' : 'Niedrigste Einzelwertung',
                              'max' : 'Höchste Einzelwertung'})
        stats = stats.rename(columns={'Punkte' : 'Alle Aufgaben'})

        stats = stats.round(2)
        return pd.DataFrame(stats.iloc[1:])
    
    def examStatistics(self):

        grades = self.grades['Note'].replace(self.gradeDict)
        stats = pd.to_numeric(grades).describe()

        # add failing statistics
        writers = (self.grades['Note'] != 'ne')
        stats['Durchfallquote [%]'] = 100*float(grades[grades == 5].shape[0]) / self.grades[writers].shape[0]

        # resort rows
        stats = stats.reindex(index = ['mean', 'std', 'Durchfallquote [%]', 'count', 'min', '25%', '50%', '75%', 'max'])

        # rename rows
        stats = stats.rename({'mean': 'Notenschnitt', 'std': 'Standardabweichung', '25%': '25%-Quantil',
                              '50%' : '50%-Quantil (Median)', '75%' : '75%-Quantil', 'min' : 'Beste Note',
                              'max' : 'Schlechteste Note', 'count' : 'Mitschreiber'})

        #empty header name 'Note' -> ''
        stats = stats.rename('')

        return pd.DataFrame(stats).round(2)

    def histogram(self, grades=False, relative=False, cumulative=False, **kwargs):
        writers = (self.grades['Note'] != 'ne')
        if grades:

            sums = pd.Series(0, index=self.gradeDict).sort_index()

            sumsActual = self.grades[writers]['Note'].value_counts()
            for key in list(sumsActual.index):
                sums[key] = sumsActual[key]

            xlabel = 'Note'
        else:
            sums = self.grades[writers]['Punkte'].value_counts().sort_index(ascending=False)
            xlabel = 'Punkte'

        if relative:
            sums = 100*sums/sums[:].sum()
            ylabel = 'Prozent'
        else:
            ylabel = 'Anzahl'

        if cumulative:
            sums = sums.cumsum()
            title = 'Kummuliertes Histogramm, ' + xlabel
        else:
            title = 'Histogramm, ' + xlabel

        sumsMax = sums[:].max()

        ax = sums.plot(color='blue', kind="bar", sort_columns=False, **kwargs)

        if relative:
            ax.set_yticks([i * sumsMax / 100 for i in range(0, 101, 5)])
        else:
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid('on', axis = 'y')

        return ax
    
    def writeCSV(self, outPath, columns = None):

        if columns is None:
            columns = list(self.grades)

        # write grades as decimals
        grades = self.grades.copy()
        if 'Note' in columns:
            grades['Note'] = grades['Note'].replace(self.gradeDict)

        grades.to_csv(outPath, columns = columns, index = False, sep = '\t')


def multi_column_df_display(list_dfs, cols=3):
    """"
    Display two (or more) pandas tables next to each other in Jupyter notebooks.
    """
    html_table = "<table style='width:100%; border:0px'>{content}</table>"
    html_row = "<tr style='border:10px'>{content}</tr>"
    html_cell = "<td style='width:{width}%;vertical-align:top;border:0px'>{{content}}</td>"
    html_cell = html_cell.format(width=100 / cols)

    cells = [html_cell.format(content=df.to_html()) for df in list_dfs]
    cells += (cols - (len(list_dfs) % cols)) * [html_cell.format(content="")]  # pad
    rows = [html_row.format(content="".join(cells[i:i + cols])) for i in range(0, len(cells), cols)]
    display(HTML(html_table.format(content="".join(rows))))


@click.command()
@click.argument('file_name', default='template')
@click.option('--to', default='html', help='Export format, can be html (default) or pdf')
@click.option('--run/--no-run', default=True, help='Execute the notebook before export (default) or not')
def export_notebook(file_name, to='html', run=True):
    """
    export a jupyter notebook to html or pdf
    """
    notebook_content = io.open(file_name, 'r', encoding='utf8').read()
    notebook = nbformat.reads(notebook_content, as_version=4)

    if run:
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(notebook, {'metadata': {'path': '.'}})

    exporter = HideCodeHTMLExporter()
    if to == 'pdf':
        exporter = HideCodePDFExporter()

    basename = os.path.splitext(file_name)[0]

    (body, resources) = exporter.from_notebook_node(notebook)
    with io.open(basename + '.' + to, 'w', encoding='utf8') as file:
        file.write(body)


@click.command()
@click.argument('file_name', default='template')
def create(file_name):
    """
    copy template notebook to current working directory
    """
    template_notebook = pkg_resources.read_text(template, 'template.ipynb')
    template_csv = pkg_resources.read_text(template, 'exam_in.csv')

    with io.open(file_name + '.ipynb', 'w', encoding='utf8') as file:
        file.write(template_notebook)
    with io.open('exam_in.csv', 'w', encoding='utf8') as file:
        file.write(template_csv)


@click.group()
def cli():
    pass


cli.add_command(create)
cli.add_command(export_notebook)


if __name__ == '__main__':
    cli()
