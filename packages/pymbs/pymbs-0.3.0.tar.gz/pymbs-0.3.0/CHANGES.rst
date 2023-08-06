==========
Change Log
==========


0.3.0
-----

Changes:
~~~~~~~~

- Version 0.3.0 introduces a new Terms Sheet format that is **NOT**
  backwards-compatible with prior versions of PyMBS. This new format stores
  tabular data as lists of dictionaries. All numerical values that are inputs
  to the model are stored as String values and converted into Python Decimal
  objects when the JSON is parsed.

  See https://docs.python.org/3/library/decimal.html for more information on
  Python's decimal module for fixed point and floating point arithmetic.


0.2.1
-----

Changes:
~~~~~~~~

- Revised the way that we deal with some exceptions so that they are handled
  gracefully across various IPython kernels, including the Jupyter Notebook.
  Exceptions encountered when used outside of IPython/Jupyter are handled
  better as well.


0.2.0
-----

Changes:
~~~~~~~~

- Changed all references to group_id to string values


0.1.5
-----

Changes:
~~~~~~~~

- Fixed an issue with missing package config/data


0.1.0
-----

Changes:
~~~~~~~~

- Significant update to Configuration management. Created new Config object
  to hold configuration settings. Provide ability to set settings via YAML
  file and/or environment variables.

- Added some basic logging, especially in the Config object.

- Significant updates to documentation.


0.0.2
-----

Changes:
~~~~~~~~

- Significant update to intital architecture, but still in alpa stage.

- Run cash flows for *Assumed Collateral* replines only.

- Implement payment functionality for the following payment rule types:
    * Calculate (*Basic* functioanlity for calulating buckets of cash)
    * Pay Accrue, for Z bond accrual
    * Pay Pro Rata
    * Pay Sequential

- Generates cash flows for any waterfall that makes use of the above rules.

- Introduces the Tranche object, to enable flexibilty when making payments
  to tranches from the waterfall. This appears to be a much better approach
  than trying to use Pandas DataFrames for this task. Once the cash flows
  have been generated for the tranche, they are converted to a DataFrame
  for display and use in a Jupyter Notebook.

- Calculate Weighted Average Lives (WALs) for all tranches in the model that
  are paid using one of the pay rules described above.


0.0.1
-----

Changes:
~~~~~~~~

- Initial version.
