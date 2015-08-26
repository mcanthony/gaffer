##########################################################################
#
#  Copyright (c) 2014, Image Engine Design Inc. All rights reserved.
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

import Gaffer
import GafferUI

Gaffer.Metadata.registerNode(

	Gaffer.ExecutableNode,

	"description",
	"""
	Base class for nodes which have external side effects - generating
	files on disk for instance. Can be connected with other executable
	nodes to define an order of execution based on dependencies between
	nodes. A Dispatcher can then be used to actually perform the execution
	of such a network.
	""",

	plugs = {

		"requirements" : (

			"description",
			"""
			Input connections to upstream nodes which must be
			executed before this node.
			""",

			"nodule:type", "GafferUI::CompoundNodule",
			"compoundNodule:spacing", 0.4,

			"plugValueWidget:type", "",

		),

		"requirement" : (

			"description",
			"""
			Output connections to downstream nodes which must
			not be executed until after this node.
			""",

			"plugValueWidget:type", "",

		),

		"dispatcher" : (

			"description",
			"""
			Container for custom plugs which dispatchers use to
			control their behaviour.
			""",

			"plugValueWidget:type", "GafferUI.LayoutPlugValueWidget",
			"layout:section", "Dispatcher",
			"layout:index", -3, # Just before the node section,
			"nodule:type", "",

		),

	}

)