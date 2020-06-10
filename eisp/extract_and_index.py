import glob
import os
from elasticsearch_dsl import connections
from tika import parser
from eisp.utils import logger, load_elastic_mapping


def get_pdf_files(path_to_dir):
    result = glob.iglob(os.path.join(path_to_dir, '**', '*.[pP][dD][fF]'))
    return result

def get_pdf_content(file):
    file_data = parser.from_file(file, 'http://tika:9998/tika')
    text = file_data['content']
    return text

def create_index(path_to_elastic_mapping):
    idxs = connections.get_connection().indices
    logger().debug('Creating index %s', 'eisp')
    idxs.create(index='eisp', body=load_elastic_mapping(path_to_elastic_mapping))

def index_pdfs(index_name, path_to_pdfs):
    pdfs = get_pdf_files(path_to_pdfs)
    for i, e in enumerate(pdfs):
        pdf_content = get_pdf_content(e)
        yield {
            "_index": index_name,
            "_id": i,
            "pdf_name": e,
            "content": pdf_content
        }





