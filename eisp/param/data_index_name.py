from distutils.util import strtobool
from typing import List

from eisp.param._param import _param
from eisp.utils import concretemethod, instance, logger


class data_sync(_param):
  '''
  todo: docs
  '''

  @concretemethod
  def _parse(self, params: List[str]) -> None:
    '''
    todo: docs
    '''
    instance.config.set('data', 'index_name', str(strtobool(params[0])))
    logger().info('Set data index_name to %r', bool(strtobool(params[0])))
