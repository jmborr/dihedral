'''
Created on Jan 10, 2014

@author: jbq
'''
import numpy
from logger import vlog

class Unit(object):
  '''
  This class implements an angle unit
  '''

  domainlenghts = { 'radian': 2*numpy.pi, 'degree': 360.0, 'gradian': 400.0, 'state_index':None }

  def __init__(self, angletype):
    '''
    Attributys:
      type
      domainlength
    '''
    if angletype in Unit.domainlenghts.keys():
      self.type = angletype
    else:
      vlog.error( 'Angle unit not recognized. Implemented units are : {0}'.format( ', '.join(Unit.domainlenghts.keys()) ) )
    self.domainlenght = Unit.domainlenghts[ angletype ]