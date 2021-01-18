# Descripción
El proyecto consiste en crear un Data Pipeline que, partiendo de los datos en la base de datos sqlite:
- data/raw/raw_data_project_m1.db

Cree una tabla como esta y guarde el resultado en un .CSV:
| Country | Job Title | Rural | Quantity | Percentage |
| --- | --- | --- | --- | --- |
| Spain | Data Scientist | countryside | 25 | 5% |
| Spain | Data Scientist | urban | 25 | 5% |
| ... | ... | ... | ... | ... |

Para eso necesitamos cruzar los datos de la base de datos con otras fuentes:
- Los paises los sacamos usando web scraping desde esta url:
https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes

- Los datos de trabajos los sacamos usando la API desde:
http://api.dataatwork.org/v1/spec/#!/default/get_jobs_id




# Instrucciones

