from math import pi, cos, sin
from random import randint
from constants import *

def getRelativePos( origin, destination ):
	return [destination[X] - origin[X], destination[Y] - origin[Y]]

def getAbsolutePos( origin, offset ):
	return [origin[X] + offset[X], origin[Y] + offset[Y]]

class PathContainer:
	def __init__( self ):
		self.paths =   {1: [ [[0,0]] ],
						2: [ [[0,0],[0,1]] ],
						3: [ [[0,0],[0,1],[0,2]], [[0,0],[0,1],[1,1]] ], #, [[0,0],[0,1],[-1,1]] ],
						4: [ [[0,0],[0,1],[0,2],[0,3]], [[0,0],[0,1],[0,2],[1,2]], [[0,0],[0,1],[1,1],[1,2]], [[0,0],[0,1],[1,1],[1,0]] ],
						5: [ [[0,0],[0,1],[0,2],[0,3],[0,4]], [[0,0],[0,1],[0,2],[0,3],[1,3]], [[0,0],[0,1],[0,2],[1,2],[1,3]], [[0,0],[0,1],[0,2],[1,2],[2,2]], [[0,0],[0,1],[0,2],[1,2],[1,1]], [[0,0],[0,1],[1,1],[1,2],[2,2]], [[0,0],[0,1],[1,1],[2,1],[2,2]], [[0,0],[0,1],[1,1],[2,1],[2,0]], [[0,0],[1,0],[1,1],[2,1],[2,0]] ],
						6: [ [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [4, 1]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [4, 1]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [3, 2]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [2, 1]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [4, 1]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [3, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [3, 0]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [3, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [1, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [0, 1]], [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 2]], [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 0]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [3, 2]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [1, 2]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 0], [3, 0]], [[0, 0], [1, 0], [1, 1], [1, 2], [2, 2], [2, 1]], [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [2, 3]], [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [0, 3]], [[0, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 1]], [[0, 0], [1, 0], [1, 1], [0, 1], [0, 2], [1, 2]] ],
						7: [ [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [5, 1]], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [4, 1], [5, 1]], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [4, 1], [4, 2]], [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [4, 1], [3, 1]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [4, 1], [5, 1]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [4, 1], [4, 2]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [4, 1], [4, 0]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [3, 2], [4, 2]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [3, 2], [3, 3]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [3, 2], [2, 2]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [2, 1], [2, 2]], [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [2, 1], [1, 1]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [4, 1], [4, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [4, 1], [4, 0]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [3, 2], [4, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [3, 2], [3, 3]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [3, 2], [2, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [3, 0], [4, 0]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [3, 2], [4, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [3, 2], [3, 3]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [3, 2], [3, 1]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [3, 3]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [1, 3]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 2], [1, 3]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 2], [1, 1]], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 2], [0, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [1, 2], [2, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [1, 2], [1, 3]], [[0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [1, 2], [0, 2]], [[0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [0, 1], [0, 2]], [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [4, 1], [4, 2]], [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [4, 1], [4, 0]], [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 2], [4, 2]], [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 2], [2, 2]], [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 0], [4, 0]], [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 0], [2, 0]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [3, 2], [3, 3]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [3, 2], [3, 1]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [2, 3], [3, 3]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [2, 3], [1, 3]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [1, 2], [1, 3]], [[0, 0], [1, 0], [1, 1], [2, 1], [2, 0], [3, 0], [3, 1]], [[0, 0], [1, 0], [1, 1], [1, 2], [2, 2], [3, 2], [3, 3]], [[0, 0], [1, 0], [1, 1], [1, 2], [2, 2], [3, 2], [3, 1]], [[0, 0], [1, 0], [1, 1], [1, 2], [2, 2], [2, 3], [1, 3]], [[0, 0], [1, 0], [1, 1], [1, 2], [2, 2], [2, 1], [3, 1]], [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [2, 3], [2, 2]], [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 4]], [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [0, 4]], [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [0, 3], [0, 2]], [[0, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 3], [1, 3]] ],
						8: []
						}
						
		self.addMirrors()
	
	def mirror( self, pos, axis=0 ):
		newPos = pos[:]
		newPos[axis] *= -1
		return newPos
	
	def mirrorPath( self, path, axis=0 ):
		return [self.mirror(pos,axis) for pos in path]
	
	def addMirrors( self ):
		for i in range(len(self.paths)):
			pathList = self.paths[i+1]
			
			newPathList = []
			for path in pathList:
				mPath = self.mirrorPath( path )
				
				if mPath == path: newPathList.append( path )
				else: newPathList.extend( [path, mPath] )
			
			self.paths[i+1] = newPathList
	
	def rotate( self, pos, angle ):
		return [ int(round(pos[X]*cos( angle ) - pos[Y]*sin( angle ))), int(round(pos[X]*sin( angle ) + pos[Y]*cos( angle ))) ]
		
	def rotatePath( self, path, angle=pi/2 ):
		return [ self.rotate( pos, angle ) for pos in path ]
		
	def getRotations( self, path ):
		return [ self.rotatePath( path, (pi/2)*i ) for i in range(4) ]
		
	def reversePath( self, path ):
		tempPath = path[:]
		tempPath.reverse()
		return [getRelativePos(tempPath[0],pos) for pos in tempPath]