"""
	solve.py (RENAME)
	~~~~~~~~~

	Solver for G52GRP Link-A-Pix Project
	
	This module implements the solving functionality for a given puzzle configuration.
	The program takes 3 arguments on the command line, and outputs the puzzle solution
	to a temp file (of name and type specified in constants.py) in the specified puzzle
	directory.
	
	Command line interface:
		$ python solver.py [PUZZLE_WIDTH] [PUZZLE_HEIGHT] [PUZZLE_NAME]
		(PUZZLE_NAME is a type-specified name of a file located in the directory specified in constants.py)
		
	:Mandla Moyo, 2014.
"""

from cellReader import Cell, CsvCellReader, JsonCellReader
from pathContainer import PathContainer
from math import pi, cos, sin
from random import randint, shuffle, choice
from grid import Grid
from pattern import getRotations, getRelativePos, getAbsolutePos, getRelativePath, getEuclidianDistance, addMirrors
from constants import *
from copy import deepcopy
import sys

GRID = 0
FREE = 1
CELLS = 2

class SolveGrid( Grid ):
	def __init__( self, x, y ):
		Grid.__init__( self, x, y )
		self.initEndCells = 0
		self.build()
		self.backTrackMap = {}
		
	def build( self ):
		for j in range( self.dimensions[Y] ):
			cells = []
			for i in range( self.dimensions[X] ):
				cell = Cell( [i,j] )
				cells.append(cell)
				self.cellList.append(cell)
			self.grid.append( cells )
	
	
	def setCellInfo( self, cellInfo ):
		"""Takes the information from a file reader, and uses it to set the values of 
		the grid's cells.
		"""
		for info in filter( lambda x: x[TYPE] == END, cellInfo ):
			cell = self.grid[ info[Y] ][ info[X] ]
			cell.setValue( info[VALUE] )
			cell.setType( info[TYPE] )
			cell.setPathIds( info[START_ID], info[END_ID] )
			cell.setColour( info[COLOUR] )
	
	
	################################ PRINTING FUNCTIONS (DEBUGGING) ############################### pathList
	
	def printGrid( self, rnge=False ):
		for j in range(len(self.grid)):
			for i in range(len(self.grid[j])):
				cell = self.grid[j][i]
				if cell.getType() == END: print cell.getValue(),
				elif cell.getType() == PATH: print cell.getValue(),#'*',
				elif rnge and self.isReachable( rnge, [i,j] ): print 'X',
				else: print ' ',
			print ''
		print ''
	
	def getInfo( self ):
		"""Prints cell information
		"""
		for j in range(len(self.grid)):
			for i in range(len(self.grid[j])):
				cell = self.grid[j][i]
				if cell.getType() != EMPTY:
					print "[%(x)d, %(y)d]:\tValue -> %(v)d, Type -> %(t)d" % {'x': i, 'y': j, 'v': cell.getValue(), 't': cell.getType()}
	
	
	def showRange( self, pos ):
		"""Prints the range of the Cell at the given position
		"""
		self.printGrid( pos )
	
	###############################################################################################
	'''
	def getCellAt( self, pos ):
		return self.grid[pos[Y]][pos[X]]
	
	def isReachable( self, p1, p2 ):
		"""Returns True if p1 reachable from p2 and visa versa.
		"""
		res = abs( p1[0]-p2[0] ) + abs( p1[Y] - p2[Y] )
		v = self.getCellAt( p1 ).getValue()

		return res < v and res%2 != v%2
	'''
	def checkValid( self ):
		"""Returns false if the board configuration violates any basic principles of complete-ability.
			Tests to make sure:
				1) There is an even number of end cells (all cells can be paired),
				2) All cells are reachable from at least one other cell of equal value.
		"""
		
		endCells = self.getCellType( END )
		
		# Even number of endpoints?
		if len( endCells ) % 2 != 0: return False
		
		# All endpoints have other reachable endpoints of equal value?
		for cell in endCells:
			if len( getReachable( cell.pos )) == 0: return False
		
		return True
	
	'''	
	def getReachable( self, pos ):
		"""Returns a list of all cells that are reachable from the Cell at the given position, that also share the same value and colour.
		"""
		cell = self.getCellAt( pos )
		valid = [c for c in self.getCellType( END ) if c.getValue() == cell.getValue() and c.cid != cell.cid and c.colour == cell.colour and self.isReachable( pos, c.getPosition() )]
		return filter( lambda c : len(self.getConnections( pos, c.getPosition() )) > 0, valid )
		
	def getCellType( self, cellType ):
		"""Returns all the cells of a particular type.
			Cell Types:
				END		- The cell is an endpoint, and is visible in the initial puzzle state.
				PATH	- The cell contains a value, but is a part of a path connecting two endpoints.
				EMPTY	- The cell contains no data, and represents a blank space in the puzzle.
		"""
				
		return [c for c in self.cellList if c.getType() == cellType]
	'''	
	def setInitEndCellCount( self ):
		self.initEndCells = self.getConnectableEndCellCount()
		#print self.initEndCells
		
	def numConnected( self ):
		"""Returns the number of unique connected paths in the current puzzle configuration.
		"""
		sids = [c.startId for c in self.getCellType( PATH )]
		eids = [c.endId for c in self.getCellType( PATH )]
		return len( set( sids + eids ))
		
	def getConnectedness( self ):
		"""Returns the percentage of the board that has been fully connected.
		"""
		connectedCells = self.numConnected()
		return connectedCells/float( len( self.getCellType( END )) + connectedCells )
		
	def getConnectableEndCellCount( self ):
		return len( filter( lambda x: x.getValue() > 2, self.getCellType( END )))
		
	def getCompleteness( self ):
		return ( self.initEndCells - self.getConnectableEndCellCount()) / float( self.initEndCells )
		
	'''	   
	def getConnections( self, startPos, endPos ):
		"""Returns the set of valid connection patterns for a given pair of endpoints.
		"""
		# Get the cells at the specified positions.
		startCell = self.getCellAt( startPos )
		endCell = self.getCellAt( endPos )
		
		# There are no valid connections if the two cells are:
		#	1) Not of equal value,
		if startCell.getValue() != endCell.getValue(): return []
		
		#	2) Not both end cells,
		if startCell.getType() == PATH or endCell.getType() == PATH: return []
		
		#	3) Not reachable from one another.
		if not self.isReachable( startPos, endPos ): return []

		valid = []
		value = startCell.getValue()
		
		# Get the possible paths for the specified value.
		distance = getEuclidianDistance( startCell.getPosition(), endCell.getPosition() )
		paths = addMirrors( self.pathList.paths[value][distance] )
		
		# Test whether each path is a valid connector of the two points:
		#  For each of the possible paths,
		for p in paths:
		
			# All the possible rotations are expanded, and for each one,
			plist = getRotations( p )
			for rp in plist:
			
				# The alignment of the rotation is checked (it's endpoints correspond to the positions of the specified points).
				if rp[-1] == getRelativePos( startPos, endPos ) or rp[-1] == getRelativePos( endPos, startPos ):
				
					# If the starting position of the rotation is not the specified start position, the rotation is reversed.
					p = rp if rp[-1] == getRelativePos( startPos, endPos ) else getRelativePath( rp )
					isValid = True
					
					# Each of the positions in the path being tested is checked for any properties that render it invalid:
					for pos in p:
						aPos = getAbsolutePos( startPos, pos )
						
						# The position must be in bounds, and either empty (not a path point or end point in another path), or
						#  one of the initially specified end points.
						if not self.isValidPos( aPos ) or (self.getCellAt( aPos ).getType() != EMPTY and  0 < p.index( pos ) < len(p)-1):
							isValid = False
							break
						
					if isValid and p not in valid: valid.append( p )
						
		return valid
	'''
	def innerConnect( self, startPos, endPos, path ):
		"""Helper function for self.connect.
		Updates the values of all the cells in a newly connected path.
		"""
		startCell = self.getCellAt( startPos )
		endCell = self.getCellAt( endPos )
	
		startCell.connected = True
		endCell.connected = True
		
		for pos in path:
			cell = self.getCellAt( getAbsolutePos( startPos, pos ))
			cell.setType( PATH )
			cell.setValue( startCell.getValue() )
			cell.startId = startCell.cid
			cell.endId = endCell.cid
			cell.colour = startCell.colour
			
	def connect( self, startPos, endPos, path ):
		"""Connects a given pair of endpoints with a specified path.
		"""
		oldGrid = self.getCellInfo()
		self.innerConnect( startPos, endPos, path )
		newGrid = self.getCellInfo()
		self.setCellInfo( oldGrid )
		return Grid( self.dimensions[X], self.dimensions[Y], newGrid )
	
	
	def getPossibleConnections( self, maxPaths=-1 ):
		# get end cells
		cells = self.getCellType( END )
		
		# for each cell
		for c in cells:
		# sort by connection count
		
		# get unconnected end cells
		# pick one with fewest connection possibilities
			targets = self.getReachable( c.getPosition() )
			
		# pick a random connection (cell,path) - pair
		
		# maintain a map of cell ids, and tried connections as invalid cells
		
	def getSimple( self ):
		"""Gets the list of unconnected end point cells that have only one possible connecting cell.
		"""
		# Get cells with only one possible connecting cell.
		cells = filter( lambda cell: len( self.getReachable( cell.getPosition() )) == 1, self.cellList )
	
		uniqueCells = []
		# Remove matching cells (one cell per pair).
		for c in cells: uniqueCells.append( c ) if self.getReachable( c.getPosition() )[0] not in uniqueCells else None
		
		# Reduce set to cells with only one possible connecting path.
		validCells = filter( lambda cell: len( self.getConnections( cell.getPosition(), self.getReachable( cell.getPosition() )[0].getPosition() )) == 1, uniqueCells )
		
		return [c.getPosition() for c in validCells]
		
	def solveSimple( self ):
		"""Uses self.getSimple() to repeatedly connect unconnected endPoints, and then update the grid
		based on the results to further narrow down the possible connections that can be made.
		"""
		simple = self.getSimple()
		
		while simple:
			for pos in simple:
				if self.getCellAt( pos ).getType() != END or not self.getReachable( pos ): continue
				target = self.getReachable( pos )[0].getPosition()
				conns = self.getConnections( pos, target )
				self.innerConnect( pos, target, conns[0] )
				
			simple = self.getSimple()
			
	
	def backtrack( self ):
		# Solve straightforward connections
		self.solveSimple()
		
		# Run backtracking procedure
		
		# stack = [[grid,possible_connections],..]
		#uniqueCells = []
		
		# Get cells with only one possible connecting cell.
		#cells = filter( lambda cell: len( self.getReachable( cell.getPosition() )) == 1, self.cellList )
		
		# Remove matching cells (one cell per pair).
		#for c in cells: uniqueCells.append( c ) if self.getReachable( c.getPosition() )[0] not in uniqueCells else None
		#freeCells = { tuple(c.getPosition()) : self.getConnections( c.getPosition(), self.getReachable( c.getPosition() )[0].getPosition() ) for c in uniqueCells }
		stack = []#[ deepcopy(self.grid), freeCells ]
		moveStack = []
		#print self.getCompleteness()
		
		while self.getCompleteness() < 1:
			#if not backtrack:
			#tempGrid = deepcopy( self.grid )# get Cell Possibilities
			#tempList = deepcopy( self.cellList )
			uniqueCells = []
			cells = filter( lambda cell: len( self.getReachable( cell.getPosition() )) == 1, self.cellList )
			for c in cells: uniqueCells.append( c ) if self.getReachable( c.getPosition() )[0] not in uniqueCells else None
			freeCells = { tuple(c.getPosition()) : self.getConnections( c.getPosition(), self.getReachable( c.getPosition() )[0].getPosition() ) for c in uniqueCells }
			
			'''
			print '--START--'
			print 'STACK TOP'
			if stack:
				for c in stack[-1][FREE]: print c, stack[-1][FREE][c], len( self.getReachable( list( c )))
			else: print '-empty-'
			print '\nCurrent possibilities'
			for c in freeCells: print c, freeCells[c], len( self.getReachable( list( c )))
			print '---\n'
			'''
			if not freeCells:
				return -1
			"""
			#backtrack = False
			while not freeCells and self.getCompleteness() < 1:
				
				print 'BACKTRACKING...'
				for i in range(len(stack)):
					print i
					self.grid = stack[i][GRID]
					self.cellList = stack[i][CELLS]
					for cl in stack[i][FREE]:
						print cl, stack[i][FREE][cl], len( self.getReachable( list( cl )))
					print '\n'
				
				#[pos,conn] = moveStack.pop()
				frame = stack.pop()
				self.grid = frame[GRID]
				freeCells = frame[FREE]
				self.cellList = frame[CELLS]
				#freeCells[pos].remove(conn)
				#if not freeCells[pos]: freeCells.pop( pos )
				
				#print 'Freecells', freeCells
				
				'''
				for i in freeCells:
					print i, freeCells[i]
				print '\n\n'
				
				for i in range(len(stack)):
					print i
					for cl in stack[i][FREE]:
						print cl, stack[i][FREE][cl]
					print '\n'
				'''
				if freeCells:
					print '--FINISHED BACKTRACKING--'
					print 'STACK TOP'
					if stack:
						for c in stack[-1][FREE]: print c, stack[-1][FREE][c]
					else: print '-empty-'
					print '\nCurrent possibilities'
					for c in freeCells: print c, freeCells[c], len( self.getReachable( list( c )))
					print '---\n'
					'''
					print '\n\nFinished'
					for i in freeCells:
						print i, freeCells[i], len( self.getReachable( list( i )))
					print '\n\n'#return -1
					'''
			"""	
			#stack.append([ deepcopy( self.grid ), freeCells, deepcopy( self.cellList )])	
			
			
			# select a move
			pos = list( choice( freeCells.keys() ))
			cell = self.getCellAt( pos )			
			reachable = self.getReachable( pos )

			
			target = reachable[0].getPosition()
			conns = freeCells[tuple(pos)]
			
			shuffle( conns )
			conn = conns.pop()
			#print 'Chosen: ', pos, conn, '\n'
			#moveStack.append( [tuple(pos),conn] )
			if not conns: freeCells.pop( tuple(pos) )
			else: freeCells[tuple(pos)] = conns
			'''
			print 'Remaining..'
			for c in freeCells: print c, freeCells[c], len( self.getReachable( list( c )))
			print '\n\n'
			'''
			#if freeCells:
				# save frame to stack
			
			
			self.innerConnect( cell.getPosition(), target, conn )
			#print self.getConnectedness(), "**************"
			#else:
			#	backtrack = True
			
		
	
g = SolveGrid( int(sys.argv[XSIZE]), int(sys.argv[YSIZE]) )
fname, ftype = sys.argv[FILENAME].split('.')

g.importGrid( fname, ftype )
g.setInitEndCellCount()
g.backtrack()
g.exportGrid( fname, ftype )
