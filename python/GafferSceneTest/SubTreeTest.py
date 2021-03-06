##########################################################################
#
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  Copyright (c) 2012-2013, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import os
import unittest

import IECore

import Gaffer
import GafferTest
import GafferScene
import GafferSceneTest

class SubTreeTest( GafferSceneTest.SceneTestCase ) :

	def testPassThrough( self ) :

		a = GafferScene.AlembicSource()
		a["fileName"].setValue( os.path.dirname( __file__ ) + "/alembicFiles/animatedCube.abc" )

		s = GafferScene.SubTree()
		s["in"].setInput( a["out"] )

		# We have to skip the test of built in sets, because our alembic file contains cameras
		# and alembic doesn't provide a means of flagging them upfront.
		self.assertSceneValid( s["out"], assertBuiltInSetsComplete = False )

		self.assertScenesEqual( a["out"], s["out"] )
		self.assertSceneHashesEqual( a["out"], s["out"] )
		self.assertTrue( a["out"].object( "/pCube1/pCubeShape1", _copy = False ).isSame( s["out"].object( "/pCube1/pCubeShape1", _copy = False ) ) )

	def testSubTree( self ) :

		a = GafferScene.AlembicSource()
		a["fileName"].setValue( os.path.dirname( __file__ ) + "/alembicFiles/animatedCube.abc" )

		s = GafferScene.SubTree()
		s["in"].setInput( a["out"] )
		s["root"].setValue( "/pCube1" )

		self.assertSceneValid( s["out"] )
		self.assertScenesEqual( s["out"], a["out"], scenePlug2PathPrefix = "/pCube1" )
		self.assertTrue( a["out"].object( "/pCube1/pCubeShape1", _copy = False ).isSame( s["out"].object( "/pCubeShape1", _copy = False ) ) )

	def testSets( self ) :

		l = GafferSceneTest.TestLight()
		g = GafferScene.Group()
		g["in"][0].setInput( l["out"] )

		self.assertSetsValid( g["out"] )

		s = GafferScene.SubTree()
		s["in"].setInput( g["out"] )
		s["root"].setValue( "/group" )

		self.assertSetsValid( s["out"] )

	def testRootHashesEqual( self ) :

		a = GafferScene.AlembicSource()
		a["fileName"].setValue( os.path.dirname( __file__ ) + "/alembicFiles/animatedCube.abc" )

		s = GafferScene.SubTree()
		s["in"].setInput( a["out"] )

		# We have to skip the test of built in sets, because our alembic file contains cameras
		# and alembic doesn't provide a means of flagging them upfront.
		self.assertSceneValid( s["out"], assertBuiltInSetsComplete = False )
		self.assertPathHashesEqual( a["out"], "/", s["out"], "/" )

	def testDisabled( self ) :

		p = GafferScene.Plane()
		g = GafferScene.Group()
		g["in"][0].setInput( p["out"] )

		s = GafferScene.SubTree()
		s["in"].setInput( g["out"] )
		s["root"].setValue( "/group" )
		s["enabled"].setValue( False )

		self.assertSceneValid( s["out"] )
		self.assertScenesEqual( s["out"], g["out"] )
		self.assertSceneHashesEqual( s["out"], g["out"] )

	def testForwardDeclarationsFromOmittedBranchAreOmitted( self ) :

		# /group
		#	/lightGroup1
		#		/light
		#	/lightGroup2
		#		/light
		#	/lightGroup
		#		/light
		#	/lightGroup10
		#		/light

		l = GafferSceneTest.TestLight()

		lg1 = GafferScene.Group()
		lg1["name"].setValue( "lightGroup1" )
		lg1["in"][0].setInput( l["out"] )

		lg2 = GafferScene.Group()
		lg2["name"].setValue( "lightGroup2" )
		lg2["in"][0].setInput( l["out"] )

		lg3 = GafferScene.Group()
		lg3["name"].setValue( "lightGroup" )
		lg3["in"][0].setInput( l["out"] )

		lg4 = GafferScene.Group()
		lg4["name"].setValue( "lightGroup10" )
		lg4["in"][0].setInput( l["out"] )

		g = GafferScene.Group()
		g["in"][0].setInput( lg1["out"] )
		g["in"][1].setInput( lg2["out"] )
		g["in"][2].setInput( lg3["out"] )
		g["in"][3].setInput( lg4["out"] )

		self.assertSetsValid( g["out"] )

		# /light

		s = GafferScene.SubTree()
		s["in"].setInput( g["out"] )
		s["root"].setValue( "/group/lightGroup1" )

		lightSet = s["out"].set( "__lights" )
		self.assertEqual( lightSet.value.paths(), [ "/light" ] )

		self.assertSetsValid( s["out"] )

		# with includeRoot == True

		s["includeRoot"].setValue( True )

		lightSet = s["out"].set( "__lights" )
		self.assertEqual( lightSet.value.paths(), [ "/lightGroup1/light" ] )

		self.assertSetsValid( s["out"] )

	def testSetsPassThroughWhenNoRoot( self ) :

		l = GafferSceneTest.TestLight()
		g = GafferScene.Group()
		g["in"][0].setInput( l["out"] )

		s = GafferScene.SubTree()
		s["in"].setInput( g["out"] )

		lightSet = s["out"].set( "__lights" )
		self.assertEqual( lightSet.value.paths(), [ "/group/light" ] )
		self.assertSetsValid( s["out"] )

		s["root"].setValue( "/" )
		lightSet = s["out"].set( "__lights" )
		self.assertEqual( lightSet.value.paths(), [ "/group/light" ] )
		self.assertSetsValid( s["out"] )

		# with includeRoot == True

		s["includeRoot"].setValue( True )

		s["root"].setValue( "" )
		lightSet = s["out"].set( "__lights" )
		self.assertEqual( lightSet.value.paths(), [ "/group/light" ] )
		self.assertSetsValid( s["out"] )

		s["root"].setValue( "/" )
		lightSet = s["out"].set( "__lights" )
		self.assertEqual( lightSet.value.paths(), [ "/group/light" ] )
		self.assertSetsValid( s["out"] )

	def testAffects( self ) :

		s = GafferScene.SubTree()

		for n in s["in"].keys() :
			a = s.affects( s["in"][n] )
			self.assertEqual( len( a ), 1 )
			self.assertTrue( a[0].isSame( s["out"][n] ) )

	def testIncludeRoot( self ) :

		a = GafferScene.AlembicSource()
		a["fileName"].setValue( os.path.dirname( __file__ ) + "/alembicFiles/animatedCube.abc" )

		s = GafferScene.SubTree()
		s["in"].setInput( a["out"] )
		s["root"].setValue( "/pCube1" )
		s["includeRoot"].setValue( True )

		self.assertSceneValid( s["out"] )

		self.assertScenesEqual( s["out"], a["out"], pathsToIgnore = [ "/", ] )
		self.assertEqual( s["out"].childNames( "/" ), IECore.InternedStringVectorData( [ "pCube1" ] ) )
		self.assertEqual( s["out"].bound( "/" ), a["out"].bound( "/pCube1" ) )

		self.assertTrue( a["out"].object( "/pCube1/pCubeShape1", _copy = False ).isSame( s["out"].object( "/pCube1/pCubeShape1", _copy = False ) ) )

	def testRootBoundWithTransformedChild( self ) :

		a = GafferScene.AlembicSource()
		a["fileName"].setValue( os.path.dirname( __file__ ) + "/alembicFiles/animatedCube.abc" )

		s = GafferScene.SubTree()
		s["in"].setInput( a["out"] )
		s["root"].setValue( "/pCube1" )
		s["includeRoot"].setValue( True )

		with Gaffer.Context() as c :

			c.setFrame( 10 )

			expectedRootBound = a["out"].bound( "/pCube1" )
			expectedRootBound = expectedRootBound.transform( a["out"].transform( "/pCube1" ) )

			self.assertEqual( s["out"].bound( "/" ), expectedRootBound )

	def testIncludeRootPassesThroughWhenNoRootSpecified( self ) :

		a = GafferScene.AlembicSource()
		a["fileName"].setValue( os.path.dirname( __file__ ) + "/alembicFiles/animatedCube.abc" )

		s = GafferScene.SubTree()
		s["in"].setInput( a["out"] )
		s["root"].setValue( "" )
		s["includeRoot"].setValue( True )

		# We have to skip the test of built in sets, because our alembic file contains cameras
		# and alembic doesn't provide a means of flagging them upfront.
		self.assertSceneValid( s["out"], assertBuiltInSetsComplete = False )

		self.assertScenesEqual( a["out"], s["out"] )
		self.assertSceneHashesEqual( a["out"], s["out"] )
		self.assertTrue( a["out"].object( "/pCube1/pCubeShape1", _copy = False ).isSame( s["out"].object( "/pCube1/pCubeShape1", _copy = False ) ) )

	def testSetsWithIncludeRoot( self ) :

		l = GafferSceneTest.TestLight()
		g = GafferScene.Group()
		g["in"][0].setInput( l["out"] )

		self.assertSetsValid( g["out"] )

		s = GafferScene.SubTree()
		s["in"].setInput( g["out"] )
		s["root"].setValue( "/group" )
		s["includeRoot"].setValue( True )

		lightSet = s["out"].set( "__lights" )
		self.assertEqual( lightSet.value.paths(), [ "/group/light" ] )
		self.assertSetsValid( s["out"] )

	def testSetsWithNoLeadingSlash( self ) :

		l = GafferSceneTest.TestLight()
		g = GafferScene.Group()
		g["in"][0].setInput( l["out"] )

		self.assertSetsValid( g["out"] )

		s = GafferScene.SubTree()
		s["in"].setInput( g["out"] )
		s["root"].setValue( "group" )

		lightSet = s["out"].set( "__lights" )
		self.assertEqual( lightSet.value.paths(), [ "/light" ] )
		self.assertSetsValid( s["out"] )

	def testSetNamesAndGlobalsPassThrough( self ) :

		l = GafferSceneTest.TestLight()
		g = GafferScene.Group()
		g["in"][0].setInput( l["out"] )

		s = GafferScene.SubTree()
		s["in"].setInput( g["out"] )
		s["root"].setValue( "group" )

		self.assertEqual( s["out"]["globals"].hash(), g["out"]["globals"].hash() )
		self.assertTrue( s["out"]["globals"].getValue( _copy = False ).isSame( g["out"]["globals"].getValue( _copy = False ) ) )

		self.assertEqual( s["out"]["setNames"].hash(), g["out"]["setNames"].hash() )
		self.assertTrue( s["out"]["setNames"].getValue( _copy = False ).isSame( g["out"]["setNames"].getValue( _copy = False ) ) )

if __name__ == "__main__":
	unittest.main()
