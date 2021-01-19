# Descripción
El proyecto consiste en crear un *pipeline* que, utilizando varias técnicas, cruce distintas fuentes de datos para enriquecer un dataset.

## Base de datos
Partimos de una base de datos sqlite que está en:

`data/raw/raw_data_project_m1.db`

Ejemplo de datos obtenidos desde esta fuente:

| normalized_job_code | country_code | Rural_Area | Quantity | Percentage |
| --- | --- | --- | --- | --- |
| fd69391dc29c83d5ad744daa57de0175 | FI | No | 1 | 0.02 |
| 004431b0c1ce29ff6145307fa23f3f98 | ES | Yes | 4 | 0.07 |
| ... | ... | ... | ... | ... |

## Web Scraping
Usando *web scraping* descargamos datos de paises y códigos de pais desde esta url:

`https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes`

Ejemplo de datos:

| country_code | country_name |
| --- | --- |
| BE  | Belgium |
| EL | Greece |
| ... | ... |

## API
Usando una llamada a API descargamos jobs y códigos normalizados desde:

`http://api.dataatwork.org/v1/spec/#!/default/get_jobs_id`

Ejemplo de datos:
| job_code | job_name |
| --- | --- |
| fd69391dc29c83d5ad744daa57de0175 | Data Transcriber |
| 004431b0c1ce29ff6145307fa23f3f98 |Data Reduction Technician |
| ... | ... |

## Resultado
El resultado es una tabla tabla que se guarda como fichero .CSV.

| Country | Job Title | Rural | Quantity | Percentage |
| --- | --- | --- | --- | --- |
| Spain | Data Scientist | yes | 25 | 5% |
| Spain | Data Scientist | no | 25 | 5% |
| ... | ... | ... | ... | ... |


# Librerias
- numpy
- request
- beautifulsoup
- sqlite
- argparse


# Instrucciones
Ejecutar desde línea de comandos:

`python main.py`

Opcionalmente puede recibir dos parámetros:

| Parámetro | Descripción |
| --- | --- |
| -c --country + código de país | Obtiene los datos de un país concreto. Si no se especifica obtiene los datos de todos los paises. |
| -o --output + ruta CSV | Guarda el resultado en la ruta indicada. Por defecto, si no se especifica, se guarda en `data/results/output.csv` |


# Estructura de directorios
```
└── project
    ├── .gitignore
    ├── README.md
    ├── main.py
    ├── notebooks
    │   ├── API_analysis.ipynb
    │   ├── database_analysis.ipynb
    │   └── web_scraping_con_beautifulsoup.ipynb
    ├── p_acquisition
    │   ├── m_career_info_acquisition.py
    │   ├── m_country_data_acquisition.py
    │   └── m_job_data_acquisition.py
    ├── p_analysis
    ├── p_reporting
    │   └── m_report_to_csv.py
    ├── p_wrangling
    └── data
        ├── raw
        ├── processed
        └── results
```

# TO-DO
Bonus.

Presentación PPT.
