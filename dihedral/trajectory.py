'''
Created on Jan 10, 2014

@author: jbq
'''

import numpy

from unit import Unit
from logger import vlog

try:
  from magic import from_file
except TypeError:
  vlog.error('Please install the python-magic package ("sudo pip install python-magic")')
  raise

class Trajectory(object):
  '''
  This class implements a trajectory of dihedral angles
  '''

  def __init__( self, ):
    '''
    Attributes:
      series: the actual values, a numpy.array
      unit: degree, radian, grad
      range: [0,360], or [-pi,pi], etc
    '''
    self.series = None
    self.unit = None
    self.range = None

  def GuessUnit( self ):
    maxvalue = max( abs(numpy.max(self.series)), abs(numpy.min(self.series)) )
    if maxvalue <= 2.0*numpy.pi:
      self.unit = Unit( 'radian' )
    elif maxvalue <= 360.0:
      self.unit = Unit( 'degree' )
    else:
      self.unit = Unit( 'grad' )

  def SetRange(self, anglerange):
    self.range = anglerange

class TrajectoryLoader(object):
  '''
  This class implements a utility to load a trajectory of dihedral angles
  '''

  def __init__(self, filename, **kwargs):
    '''
    Attributes:
     filename
    '''
    self.filename = filename
    self.__dict__.update( kwargs ) # extra options

  def GuessType(self):
    self.type = from_file(self.filename)

  def Load(self):
    ''' Load a trajectory of angles from a file. Will also try to guess the units (radian, degree,...)
    as well as range ([0,360], [-pi,pi], ..)
    '''
    if type == 'ASCII text':
      options = {'comments':'#', 'delimiter':None, 'converters':None, 'skiprows':0, 'usecols':None, 'unpack':False, 'ndmin':0}
      options.update( {key:value for key, value in self.__dict__.items() if key in self.__dict__} ) #update with passed arguments
      self.series = numpy.loadtxt(self.filenamed, type='float', **options)
      if len(self.series) > 1:
        vlog.error('Error in trajectoryLoader.Load: Multi-column file. Please specify "usecols" argument. Example: usecols = 0 will read the first column. See numpy.loadtxt for more information on allowed arguments')
        self.series=None
    else:
      vlog.error( 'Loading trajectory of type {0} not implemented yet'.format(self.type))
    self.GuessUnit()

class StateTrajectory(Trajectory):
  '''
  This class implements a trajectory where we have a series of state indexes, instead of angles
  '''

  def __init(self, periodicity):
    self.unit = Unit('state_index')
    self.unit.domainlenght = periodicity
    self.range = [0, periodicity-1]

  def Load(self, dihedral):
    ''' Translate the angle series into a state series '''
    angleseries = self.trajectory.series
    initial_angle = angleseries[0]
    current_state = dihedral.FindClosestState(initial_angle)
    current_index = current_state.stateindex
    self.series = [ current_index, ]
    for angle in angleseries[1:]:
      if not current_state.BelongsToBasin(angle):
        current_state = dihedral.FindClosestState(initial_angle)
        current_index = current_state.stateindex
      self.series.append(current_index)
    self.series = numpy.array(self.series)

  def ResidenceTimes(self, index=None):
    ''' Return the times the particle remains on each state
    Arguments:
      [index]: Save times only for state with index "index"
    '''
    times=[]
    previous_index = self.series[0]
    elapsed_time=0
    for current_index in self.series[1]:
      if current_index == previous_index:
        elapsed_time += 1
      else:
        previous_index = current_index
        if index and previous_index==index:
          times.append(elapsed_time)
        else:
          times.append(elapsed_time)
        elapsed_time = 0
    return numpy.array(times)
