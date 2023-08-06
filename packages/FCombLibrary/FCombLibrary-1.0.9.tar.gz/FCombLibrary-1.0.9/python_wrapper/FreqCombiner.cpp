//
// Created by mamu on 9/20/17.
//
//pybind includes
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/chrono.h>
//FreqCombiner includes
#include "CFreqCombinations.h"

namespace py = pybind11;

PYBIND11_MODULE(FCombLibrary, m)
{
    m.doc() = "Frequency combiner plugin"; // optional module docstring
    py::class_<FData>(m, "FData").def(py::init<int, double, double>());
    m.def("get_combinations", &get_combinations, "Retrieves all combinations from a given list of frequencies");
}