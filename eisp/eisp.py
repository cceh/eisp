from sys import argv
from os import getpid
from elasticsearch import helpers
from elasticsearch_dsl import connections
from logging import getLogger, basicConfig
from eisp.utils import logger, dotdict, instance, defaultconfig
from eisp.extract_and_index import index_pdfs, create_index
from configparser import ConfigParser

def main() -> None: eisp().main()

if __name__ == '__main__': main()

class eisp():
    '''
    todo: docs
    '''

    def __init__(self) -> None:
        '''
        todo: docs
        '''
        argv.pop(0)
        basicConfig(
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s [%(levelname)s] <%(name)s> %(message)s'
        )
        getLogger('elasticsearch').disabled = True
        getLogger('werkzeug').disabled = True

    def main(self) -> None:
        try:
            instance.config = ConfigParser()
            instance.config.read_dict(defaultconfig())
            logger().info('Started eisp with pid %s', getpid())
            conf = dotdict(instance.config['data'])
            connections.create_connection(hosts=[conf.host])
            create_index(conf.elastic_mapping)
            helpers.bulk(connections.get_connection(), index_pdfs('eisp', conf.root))


        except KeyboardInterrupt:
            print('\N{bomb}')
        except Exception as exception:
            logger().exception(exception)
        except SystemExit as exception:
            logger().critical(str(exception))
