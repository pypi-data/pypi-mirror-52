# PBGA

PacBio Genome Analysis Python toolkit.

## Install

The code is available at PyPi, therefore you can install it with pip.

```bash
pip install pbga
```

## Connect to PBGA database

The PBGA database is a H2 database, therefore primarily meant to be used with Java.
We can connect to the database from Python, if:

- Java is installed on the local machine
- the local machine runs UNIX-like OS (sorry, Windows users)

Then:
```python
from pbga import H2DbManager

with H2DbManager("path/to/sv_database.mv.db", 
                 user="sa", 
                 password="sa") as h2:
    with h2.get_connection() as conn:
        with conn.cursor() as cur:
            # do whatever you want
            cur.execute('SELECT * FROM PBGA.CLINGEN_TRIPLOSENSITIVITY;')
            for i, x in zip(range(5), cur.fetchall()):
                # print first 5 lines 
                print(x)

```

## Use Jannovar `VariantEffect`s

We can access values of Jannovar `VariantEffect` enum:

```python
import pbga.effects as pe 

ve = pe.VARIANT_EFFECTS #  get tuple with all variant effects

p = pe.get_priority('MISSENSE_VARIANT') # returns 21
```

## Quick setup of Python `logging` framework

Setting up of Python `logging` framework might be tedious. Here's a small helper function:

```python
from pbga.utils import setup_logging

# set level to INFO, create a `main.log` file use nice log message format  
setup_logging()  

```
 
## Limitations

- tested with `python>=3.6.8`
