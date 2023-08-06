# -*- encoding: utf-8 -*-
# pylint: disable=E0203,E1101,C0111
"""
@file
@brief Runtime operator.
"""
import numpy
from ._op import OpRun
from ..shape_object import ShapeObject


class ConstantOfShape(OpRun):

    atts = {'value': numpy.array([0], dtype=numpy.float32)}

    def __init__(self, onnx_node, desc=None, **options):
        OpRun.__init__(self, onnx_node, desc=desc,
                       expected_attributes=ConstantOfShape.atts,
                       **options)
        self.cst = (self.value[0]
                    if isinstance(self.value, numpy.ndarray)
                    else self.value)
        if not isinstance(self.cst, (float, numpy.float32, numpy.float64)):
            raise TypeError("cst must be a real not {}".format(type(self.cst)))

    def _run(self, data):  # pylint: disable=W0221
        res = numpy.full(tuple(data), self.cst)
        return (res, )

    def _infer_shapes(self, data):  # pylint: disable=W0221
        pref = str(hex(id(self))[2:])
        shape = ["ncof%s_%d" % (pref, i) for i in range(len(data))]
        return (ShapeObject(shape, self.cst.dtype), )
