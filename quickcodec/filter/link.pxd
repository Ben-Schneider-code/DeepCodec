cimport libav as lib

from quickcodec.filter.graph cimport Graph
from quickcodec.filter.pad cimport FilterContextPad


cdef class FilterLink:

    cdef readonly Graph graph
    cdef lib.AVFilterLink *ptr

    cdef FilterContextPad _input
    cdef FilterContextPad _output


cdef FilterLink wrap_filter_link(Graph graph, lib.AVFilterLink *ptr)
