import glob
import os
import io
from elasticsearch_dsl import connections
from tika import parser
from bs4 import BeautifulSoup
from eisp.utils import logger, load_elastic_mapping


def get_pdf_files(path_to_dir):
    result = glob.iglob(os.path.join(path_to_dir, '**', '*.[pP][dD][fF]'))
    return result


def create_index(path_to_elastic_mapping, index_name):
    idxs = connections.get_connection().indices
    logger().info('Creating index %s', index_name)
    idxs.create(index=index_name, body=load_elastic_mapping(path_to_elastic_mapping))


def delete_index(index_name):
    idxs = connections.get_connection().indices
    logger().info('Dropping index %s', index_name)
    idxs.delete(ignore=404, index=index_name)


def parse_pdf(filename):
    logger().info('Indexing %s', filename)
    pages_txt = []
    # Read PDF file
    data = parser.from_file(filename, serverEndpoint='http://tika:9998/tika', xmlContent=True)
    xhtml_data = BeautifulSoup(data['content'], features='html.parser')
    for i, content in enumerate(xhtml_data.find_all('div', attrs={'class': 'page'})):
        # Parse PDF data using TIKA (xml/html)
        # It's faster and safer to create a new buffer than truncating it
        # https://stackoverflow.com/questions/4330812/how-do-i-clear-a-stringio-object
        _buffer = io.StringIO()
        _buffer.write(str(content))
        parsed_content = parser.from_buffer(_buffer.getvalue(), serverEndpoint='http://tika:9998/tika')

        # Add pages
        if parsed_content['content']:
            text = parsed_content['content'].strip()
            text = text.splitlines(keepends=True)
            cleaned_text = []
            for i, line in enumerate(text):
                if len(line) > 2:
                    cleaned_text.append(line)
            cleaned_text = ' '.join(cleaned_text)
            pages_txt.append(cleaned_text)

    return pages_txt


def index_pdfs(index_name, path_to_pdfs):
    pdfs = get_pdf_files(path_to_pdfs)
    for i, e in enumerate(pdfs):
        pdf_content = parse_pdf(e)
        for j, c in enumerate(pdf_content):
            j += 1
            yield {
                "_index": index_name,
                "_id": str(e) + '_page_' + str(j),
                "pdf_name": e,
                "content": c
            }
