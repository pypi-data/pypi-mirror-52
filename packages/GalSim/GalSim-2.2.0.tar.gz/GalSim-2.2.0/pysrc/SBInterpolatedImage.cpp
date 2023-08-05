/* -*- c++ -*-
 * Copyright (c) 2012-2019 by the GalSim developers team on GitHub
 * https://github.com/GalSim-developers
 *
 * This file is part of GalSim: The modular galaxy image simulation toolkit.
 * https://github.com/GalSim-developers/GalSim
 *
 * GalSim is free software: redistribution and use in source and binary forms,
 * with or without modification, are permitted provided that the following
 * conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions, and the disclaimer given in the accompanying LICENSE
 *    file.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions, and the disclaimer given in the documentation
 *    and/or other materials provided with the distribution.
 */

#include "PyBind11Helper.h"
#include "SBInterpolatedImage.h"

namespace galsim {

    template <typename T, typename W>
    static void WrapTemplates(PY_MODULE& _galsim, W& wrapper)
    {
        wrapper.def(py::init<const BaseImage<T> &, const Bounds<int>&, const Bounds<int>&,
                    const Interpolant&, const Interpolant&,
                    double, double, GSParams>());

        typedef double (*cscf_func_type)(const BaseImage<T>&, double);
        GALSIM_DOT def("CalculateSizeContainingFlux", cscf_func_type(&CalculateSizeContainingFlux));
    }

    void pyExportSBInterpolatedImage(PY_MODULE& _galsim)
    {
        py::class_<SBInterpolatedImage, BP_BASES(SBProfile)> pySBInterpolatedImage(
            GALSIM_COMMA "SBInterpolatedImage" BP_NOINIT);
        pySBInterpolatedImage
            .def("calculateMaxK", &SBInterpolatedImage::calculateMaxK);
        WrapTemplates<float>(_galsim, pySBInterpolatedImage);
        WrapTemplates<double>(_galsim, pySBInterpolatedImage);

        py::class_<SBInterpolatedKImage, BP_BASES(SBProfile)> pySBInterpolatedKImage(
            GALSIM_COMMA "SBInterpolatedKImage" BP_NOINIT);
        pySBInterpolatedKImage
            .def(py::init<const BaseImage<std::complex<double> > &,
                 double, const Interpolant&, GSParams>());
    }

} // namespace galsim
