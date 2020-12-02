# Fizim

This project contains a Python [subproject](./cvm-data-processor) to obtain and
normalize financial balance data from [CVM](http://www.dados.cvm.gov.br) and
write it to a database.  Also, it provides a [JHipster](https://jhipster.tech)
Java [application](./fizz) to query the database generated.

## Install

### cvm-data-processor (Python project)

This project depends on Python 3. Make sure you have it installed. Dependencies
are managed using [poetry](https://python-poetry.org/), it can be installed via
pip and then used to download the other requirements.

```bash
$ pip install poetry
$ poetry install
```

Poetry installs dependencies in a virtual environment, that needs to be
activated afterwards. Envs are created on `~/.cache`, and can be activated by
calling

```bash
$ poetry shell
```

### Fizz (Java, JHipster project)

JHipster is a platform for generating modern Java applications. The Fizz
project was generated with JHipster. It uses Java 1.8, just ensure you have it
installed. You will also need to have `npm` installed.


## Run

It is possible to generate the database with a few commands. For that you'll have
to run the Python project and the JHipster application.

1. Open two terminals
1. In one of them, enter the `fizz/` directory and run

  ```bash
  $ docker-compose -f src/main/docker/postgresql.yml up -d
  $ ./mvnw
  ```

  This will start the database and the Java application.
1. In the other terminal, enter the poetry virtual environment and run

  ```bash
  $ python main.py cvm get
  $ python main.py cvm normalize-all
  $ python main.py export-all
  ```

  This will, respectivelly, download all data from CVM of public companies.
  Perform necessary normalization on all the files, so they are more convinient
  for being persisted. Exports all data to the database.

Done! The database is created. Now you can query all that data using the Java
application that is running at port 8090.

Try this:

Access http://localhost:8090 in your browser. Sign in as admin. Go to
Administration > API. In the "companies-resource" API, click "Try it out" and
write `ABERTO` in the `situation` parameter and click "Execute" right below all
the parameters. Down below you see the response, which looks like this:

```json
{
  "content": [
    {
      "cvmCode": 922,
      "cnpj": "04.902.979/0001-44",
      "socialDenomination": "BANCO DA AMAZÔNIA S.A.",
      "commercialDenomination": "BANCO DA AMAZONIA S.A.",
      "registerDate": "1977-07-20",
      "constitutionDate": "1942-07-09",
      "cancellationDate": null,
      "cancellationReason": null,
      "situation": "ATIVO",
      "situationStartDate": "1977-07-20",
      "sector": "INTERMEDIAÇÃO FINANCEIRA",
      "market": "BOLSA",
      "category": "Categoria A",
      "cnpjAuditor": "57.755.217/0001-29",
      "auditor": "KPMG AUDITORES INDEPENDENTES"
    },
    {
      "cvmCode": 20796,
      "cnpj": "62.232.889/0001-90",
      "socialDenomination": "BANCO DAYCOVAL S.A.",
      "commercialDenomination": "BANCO DAYCOVAL S.A.",
      "registerDate": "2007-06-27",
      "constitutionDate": "1968-08-05",
      "cancellationDate": null,
      "cancellationReason": null,
      "situation": "ATIVO",
      "situationStartDate": "2007-06-27",
      "sector": "BANCOS",
      "market": "BOLSA",
      "category": "Categoria B",
      "cnpjAuditor": "49.928.567/0001-11",
      "auditor": "DELOITTE TOUCHE TOHMATSU AUDITORES INDEPENDENTES"
    },
    {
      "cvmCode": 1023,
      "cnpj": "00.000.000/0001-91",
      "socialDenomination": "BANCO DO BRASIL S.A.",
      "commercialDenomination": "BANCO DO BRASIL S.A.",
      "registerDate": "1977-07-20",
      "constitutionDate": "1905-12-30",
      "cancellationDate": null,
      "cancellationReason": null,
      "situation": "ATIVO",
      "situationStartDate": "1977-07-20",
      "sector": "BANCOS",
      "market": "BOLSA",
      "category": "Categoria A",
      "cnpjAuditor": "57.755.217/0001-29",
      "auditor": "KPMG AUDITORES INDEPENDENTES"
    }
]
```

The `main.py` is a tool to help demonstrate the usage of the avaliable modules.
With such tool it is also possible to get the previous close price of all
companies listed in [B3](http://www.b3.com.br/pt_br/):

```bash
python main.py companies --previous-close
```

Find more information of the commands with `python main.py help`. For more
information on the Java application, see [its README](./fizz/README.md).

