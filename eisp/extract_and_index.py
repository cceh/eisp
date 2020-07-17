import glob
import os
import gc
from elasticsearch_dsl import connections
from eisp.utils import logger, load_elastic_mapping
import PyPDF2


def extract_pdf(filename):
    logger().info('Reading: %s', filename)
    with open(filename, mode='rb') as f:
        try:
            reader = PyPDF2.PdfFileReader(f)
            number_of_pages = reader.getNumPages()
            for page_number in range(number_of_pages):
                page = reader.getPage(page_number)
                yield page.extractText()
        except:
            logger().error('Could not read: %s', filename)


def get_pdf_files(path_to_dir):
    result = glob.iglob(os.path.join(path_to_dir, '**', '*.[pP][dD][fF]'), recursive=True)
    return result


def create_index(path_to_elastic_mapping, index_name):
    idxs = connections.get_connection().indices
    logger().info('Creating index %s', index_name)
    idxs.create(index=index_name, body=load_elastic_mapping(path_to_elastic_mapping))


def delete_index(index_name):
    idxs = connections.get_connection().indices
    logger().info('Dropping index %s', index_name)
    idxs.delete(ignore=404, index=index_name)


def index_pdfs(index_name, path_to_pdfs):
    pdfs = get_pdf_files(path_to_pdfs)
    for i, e in enumerate(pdfs):
        doc_name = e.replace('/var/lib/eisp/', '')
        pdf_content = extract_pdf(e)
        for j, c in enumerate(pdf_content):
            j += 1
            if c:
                yield {
                    "_index": index_name,
                    "page_id": doc_name + '_page_' + str(j),
                    "page_content": c,
                    "pdf_name": doc_name

                }
                del c
                gc.collect()

        del pdf_content
