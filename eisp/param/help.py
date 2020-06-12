from sys import exit
from typing import List

from eisp.param._param import _param
from eisp.utils import concretemethod


class help(_param):
  '''
  todo: docs
  '''

  @concretemethod
  def _parse(self, params: List[str]) -> None:
    '''
    todo: docs
    '''
    exit('Work in progress')
