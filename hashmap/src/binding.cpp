#include <pybind11/pybind11.h>
#include <torch/extension.h>

#include "hashmap.h"

using namespace py::literals;

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m)
{
    py::class_<HashMap> hashmap(m, "HashMap");
    hashmap.def(py::init<int, int, at::Tensor &>());
    hashmap.def("create_map", &HashMap::createMap, "size"_a);
}