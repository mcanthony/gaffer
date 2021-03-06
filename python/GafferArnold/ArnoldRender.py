##########################################################################
#
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
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

import IECore
import IECoreArnold

import Gaffer
import GafferScene

class ArnoldRender( GafferScene.ExecutableRender ) :

	def __init__( self, name="ArnoldRender" ) :

		GafferScene.ExecutableRender.__init__( self, name )

		self.addChild(
			Gaffer.StringPlug(
				"mode",
				Gaffer.Plug.Direction.In,
				"render",
			)
		)

		self.addChild(
			Gaffer.StringPlug(
				"fileName",
			)
		)

		self.addChild(
			Gaffer.IntPlug(
				"verbosity",
				Gaffer.Plug.Direction.In,
				2
			)
		)

	def _createRenderer( self ) :

		fileName = self.__fileName()
		directory = os.path.dirname( fileName )
		if directory :
			try :
				os.makedirs( directory )
			except OSError :
				# makedirs very unhelpfully raises an exception if
				# the directory already exists, but it might also
				# raise if it fails. we reraise only in the latter case.
				if not os.path.isdir( directory ) :
					raise

		renderer = IECoreArnold.Renderer( fileName )
		renderer.setOption( "ai:procedural_searchpath", os.path.expandvars( "$GAFFER_ROOT/arnold/procedurals" ) )

		return renderer

	def _outputWorldProcedural( self, scenePlug, renderer ) :

		# Create the ScriptProcedural that we want to load at render time.
		scriptNode = scenePlug.node().scriptNode()
		scriptContext = scriptNode.context()
		currentContext = Gaffer.Context.current()

		procedural = GafferScene.ScriptProcedural()
		procedural["fileName"].setTypedValue( scriptNode["fileName"].getValue() )
		procedural["node"].setTypedValue( scenePlug.node().relativeName( scriptNode ) )
		procedural["frame"].setNumericValue( currentContext.getFrame() )

		contextArgs = IECore.StringVectorData()
		for entry in [ k for k in currentContext.keys() if k != "frame" and not k.startswith( "ui:" ) ] :
			if entry not in scriptContext.keys() or currentContext[entry] != scriptContext[entry] :
				contextArgs.extend( [
					"-" + entry,
					 repr( currentContext[entry] )
				] )

		procedural["context"].setValue( contextArgs )

		# Output an ExternalProcedural that will load the ScriptProcedural.

		externalProcedural = IECore.Renderer.ExternalProcedural(
			"ieProcedural.so",
			IECore.Box3f( IECore.V3f( -1e30 ), IECore.V3f( 1e30 ) ),
			{
				"className" : "gaffer/script",
				"classVersion" : 1,
				"parameterValues" : IECore.StringVectorData(
					IECore.ParameterParser().serialise( procedural.parameters(), procedural.parameters().getValue() )
				)
			}
		)

		renderer.procedural( externalProcedural )

	def _command( self ) :

		mode = self["mode"].getValue()
		if mode == "render" :
			return "kick -dp -dw -v %d '%s'" % ( self["verbosity"].getValue(), self.__fileName() )
		elif mode == "expand" :
			return "kick -v %d -forceexpand -resave '%s' '%s'" % ( self["verbosity"].getValue(), self.__fileName(), self.__fileName() )

		return ""

	def __fileName( self ) :

		result = self["fileName"].getValue()
		# because execute() isn't called inside a compute(), we
		# don't get string expansions automatically, and have to
		# do them ourselves.
		## \todo Can we improve this situation?
		result = Gaffer.Context.current().substitute( result )
		return result

IECore.registerRunTimeTyped( ArnoldRender, typeName = "GafferArnold::ArnoldRender" )
