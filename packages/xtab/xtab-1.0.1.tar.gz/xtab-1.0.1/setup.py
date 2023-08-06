from distutils.core import setup

setup(name='xtab',
	version='1.0.1',
	description="Crosstabulates data in a text file.",
	author='Dreas Nielsen',
	author_email='dreas.nielsen@gmail.com',
    url='https://bitbucket.org/rdnielsen/xtab/',
	scripts=['xtab/xtab.py'],
    license='GPL',
    python_requires = '>=2.7',
	classifiers=[
		'Environment :: Console',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Topic :: Office/Business'
		],
	keywords=['CSV', 'crosstab', 'normalized', 'SQLite', 'table', 'data'],
	long_description="""``xtab.py`` is a Python module and command-line program that
rearranges data from a normalized format to a crosstabulated format. It takes data 
in this form:

======= ========== =====
Station	  Date     Value 
------- ---------- -----
WQ-01	2006-05-23  4.5
WQ-02	2006-05-23  3.7
WQ-03	2006-05-23  6.8
WQ-01	2006-06-15  9.7
WQ-02	2006-05-15  5.1
WQ-03	2006-06-15  7.2
WQ-01	2006-07-19 10
WQ-02	2006-07-19  6.1
WQ-03	2006-07-19  8.8
======= ========== =====

and rearranges it into this form:

======= ========== ========== ==========
Station	2006-05-23 2006-06-15 2006-07-19
------- ---------- ---------- ----------
WQ-01     4.5        3.7        6.8
WQ-02     9.7        5.1        7.2
WQ-03    10          6.1        8.8
======= ========== ========== ==========

Input and output are both text (CSV) files.

A summary of its capability and usage is shown below.  Full documentation
is available at http://xtab.readthedocs.org/.


Capabilities
=============

You can use the xtab program to:

* Rearrange data exported from a database to better suit its 
  subsequent usage in statistical, modeling, graphics, or other
  software, or for easier visual review and table preparation.
* Convert a single file (table) of data to a SQLite database.
* Check for multiple rows of data in a text file with the same
  key values.


Notes
======

* Multiple data values can be crosstabbed, in which case the output
  will contain multiple sets of similar columns.
* Either one or two rows of headers can be produced in the output file.
  One row is the default, and is most suitable when the output file will
  be further processed by other software.  Two rows facilitate readability
  when the output contains multiple sets of similar columns.
* The xtab program does not carry out any summarization or
  calculation on the data values, and therefore there should be
  no more than one data value to be placed in each cell of the output
  table. More than one value per cell is regarded as an error, and in
  such cases only one of the multiple values will be put in the cell.
* Error messages can be logged to either the console or a file.  If no
  error logging option is specified, then if there are multiple values
  to be put in a cell (the most likely data error), a single message
  will be printed on the console indicating that at least one error of
  this type has occurred. If an error logging option is specified,
  then the SQL for all individual cases where there are multiple values
  per cell will be logged.
* The SQL commands used to extract data from the input file for each
  output table cell can be logged to a file.
* As an intermediate step in the crostabbing process, data are converted
  to a SQLite table. By default, this table is created in memory.  
  However, it can optionally be created on disk, and preserved so that
  it is available after the crosstabulation is completed.
* There are no inherent limits to the number of rows or columns in the
  input or output files. (So the output may exceed the limits of some
  other software.)
* Input and output file names, and column names in the input file that
  are to be used for row headings, column headings, and cell values are
  all required as command-line arguments.  If any required arguments are
  missing, an exception will be raised, whatever the error logging option.
* Data rows are sorted alphanumerically by the row headers and column
  headers are sorted alphanumerically in the output.
"""
)
