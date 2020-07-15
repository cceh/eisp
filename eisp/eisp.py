from configparser import ConfigParser
from importlib import import_module as mod
from logging import getLogger, basicConfig
from os import getpid
from sys import argv
from elasticsearch import helpers
from elasticsearch_dsl import connections
from eisp.extract_and_index import index_pdfs, create_index, delete_index
from eisp.utils import logger, dotdict, instance, defaultconfig


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

    def main(self) -> None:
        try:
            instance.config = ConfigParser()
            instance.config.read_dict(defaultconfig())
            logger().info('Started eisp with pid %s', getpid())

            for i in [i for i in argv if i.startswith('--')]:
                try:
                    mod('eisp.param.{}'.format(i[2:])).__dict__[i[2:]](argv)
                except:
                    exit('Invalid parameter or argument to {}'.format(i[2:]))

            conf = dotdict(instance.config['data'])
            connections.create_connection(hosts=[conf.host])
            delete_index(conf.index_name)
            create_index(conf.elastic_mapping, conf.index_name)

            for ok, info in helpers.parallel_bulk(connections.get_connection(),
                                                  actions=index_pdfs(conf.index_name, conf.root),
                                                  request_timeout=60, chunk_size=100, thread_count=8, queue_size=8):
                if not ok:
                    print(info)

        except KeyboardInterrupt:
            print('\N{bomb}')
        except Exception as exception:
            logger().exception(exception)
        except SystemExit as exception:
            logger().critical(str(exception))
