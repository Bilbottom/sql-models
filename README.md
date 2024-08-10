<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![tests](https://github.com/Bilbottom/sql-models/actions/workflows/tests.yaml/badge.svg)](https://github.com/Bilbottom/sql-models/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/Bilbottom/sql-models)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Bilbottom/sql-models/main.svg)](https://results.pre-commit.ci/latest/github/Bilbottom/sql-models/main)
[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)

</div>

---

# SQL Models

Stand-alone SQL models.

These can be used to enhance existing databases, or as reference material for training and learning.

Some are created by me, and others are from various sources which are credited below.

## Contents

### Date Dimension

Almost all data models can be improved by adding a calendar table which has dates over a range with useful info and such, such as weekday names.

This model extends this by including holidays and additional columns.

### [Football](sql_models/football/README.md)

The Euro 2016 football tournament.

This was built by [w3resource](https://www.w3resource.com/) and can be found at:

- [https://www.w3resource.com/sql-exercises/soccer-database-exercise/index.php](https://www.w3resource.com/sql-exercises/soccer-database-exercise/index.php)

### Human Resources

Employees, departments, and salaries.

This was built by [w3resource](https://www.w3resource.com/) and can be found at:

- [https://www.w3resource.com/sql-exercises/employee-database-exercise/index.php](https://www.w3resource.com/sql-exercises/employee-database-exercise/index.php)

### [Loans](sql_models/loans/README.md)

Loans and balances for a B2B bank.

### School

A typical school.

This was built by Microsoft and can be found at:

- [https://docs.microsoft.com/en-us/ef/ef6/resources/school-database](https://docs.microsoft.com/en-us/ef/ef6/resources/school-database)

### Website Backend

A simple website with users and events.

---

Additional databases can be found at:

- https://dzone.com/articles/collection-sql-server-sample-databases
