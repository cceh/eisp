# EISP - Extract, Index and Search PDFs

EISP allows you to extract, index and search any PDF containing text.

You only have to specify in `docker-compose.yml` the folder that you would like to extract text from.

## Relevant software libraries employed:
- [Poppler](https://poppler.freedesktop.org/) 
- [pdftotext](https://pypi.org/project/pdftotext/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Kibana](https://www.elastic.co/kibana/)

## Requirements

[Docker](https://docs.docker.com/engine/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)

## Deploy

`docker-compose up`

Detached:

`docker-compose up -d`

## Search 

### Access Kibana
Go to http://0.0.0.0:5601/eisp

In Kibana on the left pane, select 'Discover' and create an index pattern for the 'eisp' index.
To search on the selected index, once again, on the left pane click on 'Discover'.



