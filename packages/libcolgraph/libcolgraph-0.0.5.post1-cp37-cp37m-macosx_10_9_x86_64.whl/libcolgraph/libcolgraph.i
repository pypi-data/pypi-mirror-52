/* libcolgraph.i */

%module libcolgraph

%include "exception.i"

%include "swigsources/wrapped_exceptions.i"
%include "swigsources/pyoverrides.i"
%include "swigsources/cpp_inline.i"
%include "swigsources/template_defs.i"

%include "GraphTemplates.h"
%include "Graph.h"
%include "Vertex.h"
