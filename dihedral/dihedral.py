'''
Created on Jan 10, 2014

@author: jbq
'''
import numpy
from trajectory import TrajectoryLoader, StateTrajectory
from state import State

class Dihedral( object ):
  '''
  This class implements a dihedral angle
  '''


  def __init__( self ):
    '''
    Attributes:
      label
      states
      periodicity
      trajectory:
    Properties
      range
    '''
    self.label = None
    self.states = None
    self.periodicity = None
    self.trajectory = None

  def SetLabel( self, label ):
    self.label = label

  def GetRange(self):
    return self.trajectory.range
  range = property(fget = GetRange)

  @property
  def range(self):
    return self.GetRange

  def SetRange(self, anglerange):
    self.trajectory.SetRange(anglerange)

  @range.setter
  def range(self, anglerange):
    self.SetRange(anglerange)

  def SetPeriodicity( self, periodicity):
    self.periodicity = periodicity

  def SetStates(self, minimum):
    '''Generate the states based on one minimum and the periodicity
    '''
    st = State(minimum)
    st.SetBasin( self.periodicity, self.range )
    self.AppendState(st)

  def AppendState( self, state ):
    self.states = [ state, ] if not self.states else self.states.append( state )

  def LoadTrajectory( self, filename, **kwargs ):
    loader =  TrajectoryLoader( filename, kwargs)
    self.trajectory = loader.LoadTrajectory()

  def GenerateStateTrajectory(self):
    statetraj = StateTrajectory(self.periodicity)
    statetraj.Load(self)
    return statetraj