'''
Created on Jan 10, 2014

@author: jbq
'''

class State(object):
  '''
  This class implements one of the dihedral minima
  '''


  def __init__(self, centroid):
    '''
    Attributes:
      centroid: 
      basin: 
    '''
    self.centroid = centroid

  def SetBasin( self, periodicity, anglerange ):
    '''The angle domain associated to each state. It's either one or two
    disconnected domains
    '''
    domainlength = anglerange[1]-anglerange[0]
    minangle = self.centroid - domainlength/(2.0*periodicity)
    maxangle = self.centroid + domainlength/(2.0*periodicity)
    if minangle < anglerange[0]:
      basin = [anglerange[0], maxangle]
      basin.append( [anglerange[1]-(anglerange[0]-minangle), anglerange[1]] )
    elif maxangle > anglerange[1]:
      basin = [anglerange[0], anglerange[0]+(maxangle-anglerange[1])]
      basin = [minangle, anglerange[1]]
    else:
      basin = [minangle, maxangle]