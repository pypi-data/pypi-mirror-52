# Datasetmaker
[![image](https://img.shields.io/pypi/v/datasetmaker.svg)](https://pypi.org/project/datasetmaker/)
[![Build Status](https://travis-ci.com/datastory-org/datasetmaker.svg?token=V6phAxmvf7gFqpigH6TT&branch=master)](https://travis-ci.com/datastory-org/datasetmaker)

Datasetmaker is Datastory's toolkit for fetching, standardizing, and packaging data.

It is composed of a number of "clients", each mapping to a data source. Every client can `get()` and `save()` data. The output adheres to the [DDF data model](https://open-numbers.github.io/ddf.html). These data packages can in turn be merged into multi-source DDF packages.

## Get started

```bash
>>> git clone git@github.com:datastory-org/datasetmaker.git
>>> make init
```

## Run tests

```bash
>>> make test
```

## Creating a new client

To add support for a new data source, a new `client` has to be created. Clients are subclasses of `Client` in datasetmaker/models. The methods `get` and `save` must be overridden. Additional methods and helper functions may be added. The basic structure is:

```python
from datasetmaker.models import Client

class MyNewClient(Client):
    def get(self, indicators, periods):
        pass
    
    def save(self, path):
        pass
```

The `get` method should fetch the data, standardize it, add it as an attribute (`data`) of the client instance and return it. Whenever possible, the user should be able to specify which indicators and time periods to fetch.

Standardization should be done using existing helper functions in datasetmaker. For example, to convert a list of country names to country codes:

```python
from datasetmaker.entity import Country

country_names = ['Sweden', 'Albania']
name_to_id = Country.name_to_id()
country_codes = [name_to_id[x] for x in country_names]
```

The `save` method is responsible for the logic of exporting the data to a DDF package.

Make sure all concepts in the dataset are available in the ontology (see below).


### Adding new canonical entities and concepts

[ to be described ]


## Creating datastory-core

To merge existing packages, use the `merge_packages` function. Assuming two DDF packages called wikipedia and worldbank exist:

```python
import datasetmaker

datasetmaker.merge_packages(['wikipedia', 'worldbank'], dest='datastory-core')
```


## Datastory Ontology

[ to be described ]


## DDF Organization

[ to be described ]


## datapackage.json

This is the format of the datapackage.json.

```
"name": "world-bank" // used as ID and SLUG. Should follow format 'my-source'
"title": "World Bank" // title of data source
"status" : "published", // "draft"
"tags" : "education, sweden, swedish-education" //comma-separated tag IDs, based on canonical list (WikiData)
"language": {
   "id": "en" //use same locales as Datastory, 2 letter codes or specific code if we need to support a very custom language
},
"default-indicator" : "life_expectancy", //optional helper for users who browse
"default-primary-key" : "country-year", //optional helper to show nice data default
"translations": [
    {
        "id": "ar",
    },
    {
        "id": "es"
    },
    {
        "id": "fr"
    }
],  
"license": "", 
"author": "Datastory", (or original if simply copy / paste)
"source" : "Skolverket" // shorthand if all indicators in dataset come from same source
"created": "2018-11-04T08:25:30.708697+00:00", //gets added automatically
resources : [] //gets added automatically
ddfSchema : [] //gets added automatically
```


If a source has many subcollections, we can allow this but should ideally be avoided: (another option is as meta data in concepts.csv)

```
"name": "world-bank-wdi" // 
"title": "World Bank – World development indicators" // title of collection
```

## /lang folder

[tbd]

## ddf--concepts--*.csv

A concept row has to include:
- concept
- concept_type
- name 

In addition, concept rows can define:
- collections ("World Development Indicators, Partisympatiundersölningen" etc.)
- tags ("agriculture, politics")
- description
- name_datastory (will override name)
- slug (will be used as slug, otherwise default to concept)
- source
- source_url
- updated
- unit
- scales [linear, log] (if there's a preferred default)


## ddf--entities--*.csv

An entitity row has to include:
- country (or whatever is the primary key, examples: school, region, organization)
- name 


In addition, an entity row can define:
- entity-domain columns (country belongs to region etc.) 
- string-type columns (for example capital name)
```
