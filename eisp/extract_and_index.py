import glob
import os
from elasticsearch_dsl import connections
import fitz
from eisp.utils import logger, load_elastic_mapping


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


def parse(filename):
    doc = fitz.open(filename)
    pages = []
    number_of_pages = doc.pageCount
    for page_number in range(number_of_pages):
        page = doc.loadPage(page_number)
        page_content = page.getText("text")
        if page_content:
            pages.append(page_content)
    return pages


def index_pdfs(index_name, path_to_pdfs):
    pdfs = get_pdf_files(path_to_pdfs)
    for i, e in enumerate(pdfs):
        doc_name = e.replace('/var/lib/eisp/', '')
        try:
            pdf_content = parse(e)
        except RuntimeError:
            logger().error('Problems indexing: %s', doc_name)
            continue
        for j, c in enumerate(pdf_content):
            j += 1

            yield {
                "_index": index_name,
                "_id": doc_name + '_page_' + str(j),
                "pdf_name": doc_name,
                "content": c
            }
        logger().info('Indexed: %s', e)
