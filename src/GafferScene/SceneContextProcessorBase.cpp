//////////////////////////////////////////////////////////////////////////
//  
//  Copyright (c) 2012, John Haddon. All rights reserved.
//  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
//  
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//  
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//  
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//  
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//  
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//  
//////////////////////////////////////////////////////////////////////////

#include "IECore/Exception.h"

#include "GafferScene/SceneContextProcessorBase.h"

using namespace IECore;
using namespace Gaffer;
using namespace GafferScene;

IE_CORE_DEFINERUNTIMETYPED( SceneContextProcessorBase );

SceneContextProcessorBase::SceneContextProcessorBase( const std::string &name )
	:	SceneProcessor( name )
{
}

SceneContextProcessorBase::~SceneContextProcessorBase()
{
}

void SceneContextProcessorBase::hashBound( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent, IECore::MurmurHash &h ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::hashBound" );
}

void SceneContextProcessorBase::hashTransform( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent, IECore::MurmurHash &h ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::hashTransform" );
}

void SceneContextProcessorBase::hashAttributes( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent, IECore::MurmurHash &h ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::hashAttributes" );
}

void SceneContextProcessorBase::hashObject( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent, IECore::MurmurHash &h ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::hashObject" );
}

void SceneContextProcessorBase::hashChildNames( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent, IECore::MurmurHash &h ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::hashChildNames" );
}

void SceneContextProcessorBase::hashGlobals( const Gaffer::Context *context, const ScenePlug *parent, IECore::MurmurHash &h ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::hashGlobals" );
}
		
Imath::Box3f SceneContextProcessorBase::computeBound( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::computeBound" );
}

Imath::M44f SceneContextProcessorBase::computeTransform( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::computeTransform" );
}

IECore::ConstCompoundObjectPtr SceneContextProcessorBase::computeAttributes( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::computeAttributes" );
}

IECore::ConstObjectPtr SceneContextProcessorBase::computeObject( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::computeObject" );
}

IECore::ConstInternedStringVectorDataPtr SceneContextProcessorBase::computeChildNames( const ScenePath &path, const Gaffer::Context *context, const ScenePlug *parent ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::computeChildNames" );
}

IECore::ConstCompoundObjectPtr SceneContextProcessorBase::computeGlobals( const Gaffer::Context *context, const ScenePlug *parent ) const
{
	throw Exception( "Unexpected call to SceneContextProcessorBase::computeGlobals" );
}