# PBGA

<u>P</u>ac<u>B</u>io <u>G</u>enome <u>A</u>nalysis Python toolkit.

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
