// Inspired from 
// https://github.com/microsoft/onnxruntime/blob/master/onnxruntime/core/providers/cpu/ml/tree_ensemble_regressor.cc.

#if !defined(_CRT_SECURE_NO_WARNINGS)
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <vector>
#include <thread>
#include <iterator>

#ifndef SKIP_PYTHON
//#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
//#include <numpy/arrayobject.h>

#if USE_OPENMP
#include <omp.h>
#endif

namespace py = pybind11;
#endif

#include "op_common_.hpp"

template<typename NTYPE>
class RuntimeTreeEnsembleRegressor
{
    public:

        // tree_ensemble_regressor.h
        std::vector<int64_t> nodes_treeids_;
        std::vector<int64_t> nodes_nodeids_;
        std::vector<int64_t> nodes_featureids_;
        std::vector<NTYPE> nodes_values_;
        std::vector<NTYPE> nodes_hitrates_;
        std::vector<NODE_MODE> nodes_modes_;
        std::vector<int64_t> nodes_truenodeids_;
        std::vector<int64_t> nodes_falsenodeids_;
        std::vector<int64_t> missing_tracks_true_;

        std::vector<int64_t> target_nodeids_;
        std::vector<int64_t> target_treeids_;
        std::vector<int64_t> target_ids_;
        std::vector<NTYPE> target_weights_;

        std::vector<NTYPE> base_values_;
        int64_t n_targets_;
        POST_EVAL_TRANSFORM post_transform_;
        AGGREGATE_FUNCTION aggregate_function_;
        std::vector<std::tuple<int64_t, int64_t, int64_t, NTYPE>> leafnode_data_;
        std::unordered_map<int64_t, size_t> leafdata_map_;
        std::vector<int64_t> roots_;
        int64_t offset_;
        int64_t max_tree_depth_;
        const int64_t four_billion_ = 4000000000L;
    
    public:
        
        RuntimeTreeEnsembleRegressor();
        ~RuntimeTreeEnsembleRegressor();

        void init(
            const std::string &aggregate_function,
            py::array_t<NTYPE> base_values,
            int64_t n_targets,
            py::array_t<int64_t> nodes_falsenodeids,
            py::array_t<int64_t> nodes_featureids,
            py::array_t<NTYPE> nodes_hitrates,
            py::array_t<int64_t> nodes_missing_value_tracks_true,
            const std::vector<std::string>& nodes_modes,
            py::array_t<int64_t> nodes_nodeids,
            py::array_t<int64_t> nodes_treeids,
            py::array_t<int64_t> nodes_truenodeids,
            py::array_t<NTYPE> nodes_values,
            const std::string& post_transform,
            py::array_t<int64_t> target_ids,
            py::array_t<int64_t> target_nodeids,
            py::array_t<int64_t> target_treeids,
            py::array_t<NTYPE> target_weights
        );
        
        py::array_t<NTYPE> compute(py::array_t<NTYPE> X) const;

        void ProcessTreeNode(std::unordered_map <int64_t, std::tuple<NTYPE, NTYPE, NTYPE>>& classes,
                             int64_t treeindex,
                             const NTYPE* x_data,
                             int64_t feature_base) const;
    
        std::string runtime_options();

        int omp_get_max_threads();
        
        py::array_t<int> debug_threshold(py::array_t<NTYPE> values) const;

        py::array_t<NTYPE> compute_tree_outputs(py::array_t<NTYPE> values) const;

private:

        void Initialize();
    
        void compute_gil_free(const std::vector<int64_t>& x_dims, int64_t N, int64_t stride,
                              const py::array_t<NTYPE>& X, py::array_t<NTYPE>& Z) const;
};


template<typename NTYPE>
RuntimeTreeEnsembleRegressor<NTYPE>::RuntimeTreeEnsembleRegressor() {
}


template<typename NTYPE>
RuntimeTreeEnsembleRegressor<NTYPE>::~RuntimeTreeEnsembleRegressor() {
}


template<typename NTYPE>
std::string RuntimeTreeEnsembleRegressor<NTYPE>::runtime_options() {
    std::string res;
#ifdef USE_OPENMP
    res += "OPENMP";
#endif
    return res;
}


template<typename NTYPE>
int RuntimeTreeEnsembleRegressor<NTYPE>::omp_get_max_threads() {
#if USE_OPENMP
    return ::omp_get_max_threads();
#else
    return 1;
#endif
}


template<typename NTYPE>
void RuntimeTreeEnsembleRegressor<NTYPE>::init(
            const std::string &aggregate_function,
            py::array_t<NTYPE> base_values,
            int64_t n_targets,
            py::array_t<int64_t> nodes_falsenodeids,
            py::array_t<int64_t> nodes_featureids,
            py::array_t<NTYPE> nodes_hitrates,
            py::array_t<int64_t> nodes_missing_value_tracks_true,
            const std::vector<std::string>& nodes_modes,
            py::array_t<int64_t> nodes_nodeids,
            py::array_t<int64_t> nodes_treeids,
            py::array_t<int64_t> nodes_truenodeids,
            py::array_t<NTYPE> nodes_values,
            const std::string& post_transform,
            py::array_t<int64_t> target_ids,
            py::array_t<int64_t> target_nodeids,
            py::array_t<int64_t> target_treeids,
            py::array_t<NTYPE> target_weights
    ) {
    aggregate_function_ = to_AGGREGATE_FUNCTION(aggregate_function);        
    array2vector(base_values_, base_values, NTYPE);
    n_targets_ = n_targets;        
    array2vector(nodes_falsenodeids_, nodes_falsenodeids, int64_t);
    array2vector(nodes_featureids_, nodes_featureids, int64_t);
    array2vector(nodes_hitrates_, nodes_hitrates, NTYPE);
    array2vector(missing_tracks_true_, nodes_missing_value_tracks_true, int64_t);
    array2vector(nodes_truenodeids_, nodes_truenodeids, int64_t);
    //nodes_modes_names_ = nodes_modes;
    array2vector(nodes_nodeids_, nodes_nodeids, int64_t);
    array2vector(nodes_treeids_, nodes_treeids, int64_t);
    array2vector(nodes_truenodeids_, nodes_truenodeids, int64_t);
    array2vector(nodes_values_, nodes_values, NTYPE);
    array2vector(nodes_truenodeids_, nodes_truenodeids, int64_t);
    post_transform_ = to_POST_EVAL_TRANSFORM(post_transform);
    array2vector(target_ids_, target_ids, int64_t);
    array2vector(target_nodeids_, target_nodeids, int64_t);
    array2vector(target_treeids_, target_treeids, int64_t);
    array2vector(target_weights_, target_weights, NTYPE);

    // additional members
    nodes_modes_.resize(nodes_modes.size());
    for(size_t i = 0; i < nodes_modes.size(); ++i)
        nodes_modes_[i] = to_NODE_MODE(nodes_modes[i]);

    Initialize();
}


template<typename NTYPE>
void RuntimeTreeEnsembleRegressor<NTYPE>::Initialize() {
  int64_t current_tree_id = 1234567891L;
  std::vector<int64_t> tree_offsets;

  for (size_t i = 0; i < nodes_treeids_.size(); i++) {
    if (nodes_treeids_[i] != current_tree_id) {
      tree_offsets.push_back(nodes_nodeids_[i]);
      current_tree_id = nodes_treeids_[i];
    }
    int64_t offset = tree_offsets[tree_offsets.size() - 1];
    nodes_nodeids_[i] = nodes_nodeids_[i] - offset;
    if (nodes_falsenodeids_[i] >= 0)
      nodes_falsenodeids_[i] = nodes_falsenodeids_[i] - offset;
    if (nodes_truenodeids_[i] >= 0)
      nodes_truenodeids_[i] = nodes_truenodeids_[i] - offset;
  }
  for (size_t i = 0; i < target_nodeids_.size(); i++) {
    int64_t offset = tree_offsets[target_treeids_[i]];
    target_nodeids_[i] = target_nodeids_[i] - offset;
  }

  max_tree_depth_ = 1000;
  offset_ = four_billion_;
  //leafnode data, these are the votes that leaves do
  for (size_t i = 0; i < target_nodeids_.size(); i++) {
    leafnode_data_.push_back(std::make_tuple(target_treeids_[i], target_nodeids_[i], target_ids_[i], target_weights_[i]));
  }
  
  std::sort(std::begin(leafnode_data_), std::end(leafnode_data_), 
    [](const std::tuple<int64_t, int64_t, int64_t, NTYPE>& t1,
       const std::tuple<int64_t, int64_t, int64_t, NTYPE>& t2) {
        if (std::get<0>(t1) != std::get<0>(t2))
            return std::get<0>(t1) < std::get<0>(t2);

        return std::get<1>(t1) < std::get<1>(t2);
  });
  
  //make an index so we can find the leafnode data quickly when evaluating
  int64_t field0 = -1;
  int64_t field1 = -1;
  for (size_t i = 0; i < leafnode_data_.size(); i++) {
    int64_t id0 = std::get<0>(leafnode_data_[i]);
    int64_t id1 = std::get<1>(leafnode_data_[i]);
    if (id0 != field0 || id1 != field1) {
      int64_t id = id0 * four_billion_ + id1;
      auto p3 = std::make_pair(id, i);  // position is i
      leafdata_map_.insert(p3);
      field0 = id;
      field1 = static_cast<int64_t>(i);
    }
  }
  //treenode ids, some are roots, and roots have no parents
  std::unordered_map<int64_t, size_t> parents;  //holds count of all who point to you
  std::unordered_map<int64_t, size_t> indices;
  std::unordered_map<int64_t, size_t> tree_ids;
  //add all the nodes to a map, and the ones that have parents are not roots
  std::unordered_map<int64_t, size_t>::iterator it;
  size_t start_counter = 0L;
  for (size_t i = 0; i < nodes_treeids_.size(); i++) {
    //make an index to look up later
    int64_t id = nodes_treeids_[i] * four_billion_ + nodes_nodeids_[i];
    auto p3 = std::make_pair(id, i);  // i is the position
    indices.insert(p3);
    tree_ids.insert(std::make_pair(id, nodes_treeids_[i]));
    it = parents.find(id);
    if (it == parents.end()) {
      //start counter at 0
      auto p1 = std::make_pair(id, start_counter);
      parents.insert(p1);
    }
  }
  //all true nodes aren't roots
  for (size_t i = 0; i < nodes_truenodeids_.size(); i++) {
    if (nodes_modes_[i] == NODE_MODE::LEAF)
      continue;
    //they must be in the same tree
    int64_t id = nodes_treeids_[i] * offset_ + nodes_truenodeids_[i];
    it = parents.find(id);
    it->second++;
  }
  //all false nodes aren't roots
  for (size_t i = 0; i < nodes_falsenodeids_.size(); i++) {
    if (nodes_modes_[i] == NODE_MODE::LEAF)
      continue;
    //they must be in the same tree
    int64_t id = nodes_treeids_[i] * offset_ + nodes_falsenodeids_[i];
    it = parents.find(id);
    it->second++;
  }
  //find all the nodes that dont have other nodes pointing at them
  for (auto& parent : parents) {
    if (parent.second == 0) {
      int64_t id = parent.first;
      it = indices.find(id);
      roots_.push_back(it->second);
    }
  }
  // bad implementation, one loop is enough.
  int tid;
  for (auto& parent : parents) {
    if (parent.second == 0) {
      int64_t id = parent.first;
      it = indices.find(id);
      tid = tree_ids.find(id)->second;
      roots_[tid] = it->second;
    }
  }
}


template<typename NTYPE>
py::array_t<NTYPE> RuntimeTreeEnsembleRegressor<NTYPE>::compute(py::array_t<NTYPE> X) const {
    // const Tensor& X = *context->Input<Tensor>(0);
    // const TensorShape& x_shape = X.Shape();    
    std::vector<int64_t> x_dims;
    arrayshape2vector(x_dims, X);
    if (x_dims.size() != 2)
        throw std::runtime_error("X must have 2 dimensions.");

    // Does not handle 3D tensors
    int64_t stride = x_dims.size() == 1 ? x_dims[0] : x_dims[1];  
    int64_t N = x_dims.size() == 1 ? 1 : x_dims[0];

    // Tensor* Y = context->Output(0, TensorShape({N}));
    // auto* Z = context->Output(1, TensorShape({N, class_count_}));
    py::array_t<NTYPE> Z(x_dims[0] * n_targets_);

    {
        py::gil_scoped_release release;
        compute_gil_free(x_dims, N, stride, X, Z);
    }
    return Z;
}


py::detail::unchecked_mutable_reference<float, 1> _mutable_unchecked1(py::array_t<float>& Z) {
    return Z.mutable_unchecked<1>();
}


py::detail::unchecked_mutable_reference<double, 1> _mutable_unchecked1(py::array_t<double>& Z) {
    return Z.mutable_unchecked<1>();
}


template<typename NTYPE>
void RuntimeTreeEnsembleRegressor<NTYPE>::compute_gil_free(
                const std::vector<int64_t>& x_dims, int64_t N, int64_t stride,
                const py::array_t<NTYPE>& X, py::array_t<NTYPE>& Z) const {

    // expected primary-expression before ')' token
    auto Z_ = _mutable_unchecked1(Z); // Z.mutable_unchecked<(size_t)1>();
                    
    const NTYPE* x_data = X.data(0);
                    
#ifdef USE_OPENMP
#pragma omp parallel for
#endif
  for (int64_t i = 0; i < N; i++)  //for each class
  {
    int64_t current_weight_0 = i * stride;
    std::unordered_map<int64_t, std::tuple<NTYPE, NTYPE, NTYPE>> scores; // sum, min, max
    //for each tree
    for (size_t j = 0; j < roots_.size(); j++) {
      //walk each tree from its root
      ProcessTreeNode(scores, roots_[j], x_data, current_weight_0);
      // printf(" i=%d: tree %d: %f, %f, %f\n", i, j, 
      //           std::get<0>(scores[0]), std::get<1>(scores[0]), std::get<2>(scores[0]));
    }
    //find aggregate, could use a heap here if there are many classes
    std::vector<NTYPE> outputs;
    for (int64_t j = 0; j < n_targets_; j++) {
      //reweight scores based on number of voters
      auto it_scores = scores.find(j);
      NTYPE val = base_values_.size() == (size_t)n_targets_ ? base_values_[j] : 0.f;
      if (it_scores != scores.end()) {
        if (aggregate_function_ == AGGREGATE_FUNCTION::AVERAGE) {
          val += std::get<0>(scores[j]) / roots_.size();   //first element of tuple is already a sum
        } else if (aggregate_function_ == AGGREGATE_FUNCTION::SUM) {
          val += std::get<0>(scores[j]);
        } else if (aggregate_function_ == AGGREGATE_FUNCTION::MIN) {
          val += std::get<1>(scores[j]);  // second element of tuple is min
        } else if (aggregate_function_ == AGGREGATE_FUNCTION::MAX) {
          val += std::get<2>(scores[j]);  // third element of tuple is max
        }
      }
      // printf("-i=%d val=%f\n", i, val);
      outputs.push_back(val);
    }
    write_scores(outputs, post_transform_, (NTYPE*)Z_.data(i * n_targets_), -1);
  }
}


template<typename NTYPE>
void RuntimeTreeEnsembleRegressor<NTYPE>::ProcessTreeNode(
        std::unordered_map < int64_t, std::tuple<NTYPE, NTYPE, NTYPE>>& classes,
        int64_t treeindex,
        const NTYPE* x_data,
        int64_t feature_base) const {
  //walk down tree to the leaf
  auto mode = nodes_modes_[treeindex];
  int64_t loopcount = 0;
  int64_t root = treeindex;
  while (mode != NODE_MODE::LEAF) {
    NTYPE val = x_data[feature_base + nodes_featureids_[treeindex]];
    bool tracktrue = missing_tracks_true_.size() != nodes_truenodeids_.size()
                     ? false
                     : (missing_tracks_true_[treeindex] != 0) && std::isnan(val);
    NTYPE threshold = nodes_values_[treeindex];
    switch(mode) {
        case NODE_MODE::BRANCH_LEQ:
            treeindex = val <= threshold || tracktrue 
                        ? nodes_truenodeids_[treeindex]
                        : nodes_falsenodeids_[treeindex];
            break;
        case NODE_MODE::BRANCH_LT:
            treeindex = val < threshold || tracktrue
                        ? nodes_truenodeids_[treeindex]
                        : nodes_falsenodeids_[treeindex];
            break;
        case NODE_MODE::BRANCH_GTE:
            treeindex = val >= threshold || tracktrue
                        ? nodes_truenodeids_[treeindex]
                        : nodes_falsenodeids_[treeindex];
            break;
        case NODE_MODE::BRANCH_GT:
            treeindex = val > threshold || tracktrue
                        ? nodes_truenodeids_[treeindex]
                        : nodes_falsenodeids_[treeindex];
            break;
        case NODE_MODE::BRANCH_EQ:
            treeindex = val == threshold || tracktrue
                        ? nodes_truenodeids_[treeindex]
                        : nodes_falsenodeids_[treeindex];
            break;
        case NODE_MODE::BRANCH_NEQ:
            treeindex = val != threshold || tracktrue
                        ? nodes_truenodeids_[treeindex]
                        : nodes_falsenodeids_[treeindex];
            break;
        default:
            throw std::runtime_error("unknown node mode");
    }

    if (treeindex < 0) {
      throw std::runtime_error("treeindex evaluated to a negative value, which should not happen.");
    }
    treeindex = treeindex + root;
    mode = nodes_modes_[treeindex];
    loopcount++;
    if (loopcount > max_tree_depth_) 
      break;
  }
  //should be at leaf
  int64_t id = nodes_treeids_[treeindex] * four_billion_ + nodes_nodeids_[treeindex];
  //auto it_lp = leafdata_map.find(id);
  auto it_lp = leafdata_map_.find(id);
  if (it_lp != leafdata_map_.end()) {
    size_t index = it_lp->second;
    int64_t treeid = std::get<0>(leafnode_data_[index]);
    int64_t nodeid = std::get<1>(leafnode_data_[index]);
    while (treeid == nodes_treeids_[treeindex] && nodeid == nodes_nodeids_[treeindex]) {
      int64_t classid = std::get<2>(leafnode_data_[index]);
      NTYPE weight = std::get<3>(leafnode_data_[index]);
      auto it_classes = classes.find(classid);
      if (it_classes != classes.end()) {
        auto& tuple = it_classes->second;
        std::get<0>(tuple) += weight;
        if (weight < std::get<1>(tuple)) std::get<1>(tuple) = weight;
        if (weight > std::get<2>(tuple)) std::get<2>(tuple) = weight;
      } else {
        std::tuple<NTYPE, NTYPE, NTYPE> tuple = std::make_tuple(weight, weight, weight);
        auto p1 = std::make_pair(classid, tuple);
        classes.insert(p1);
      }
      index++;
      if (index >= leafnode_data_.size()) {
        break;
      }
      treeid = std::get<0>(leafnode_data_[index]);
      nodeid = std::get<1>(leafnode_data_[index]);
    }
  }
}


template<typename NTYPE>
py::array_t<int> RuntimeTreeEnsembleRegressor<NTYPE>::debug_threshold(py::array_t<NTYPE> values) const {
    std::vector<int> result(values.size() * nodes_values_.size());
    const NTYPE* x_data = values.data(0);
    const NTYPE* end = x_data + values.size();
    const NTYPE* pv;
    auto itb = result.begin();
    for(auto it = nodes_values_.begin(); it != nodes_values_.end(); ++it)
        for(pv=x_data; pv != end; ++pv, ++itb)
            *itb = *pv <= *it ? 1 : 0;
            // { *itb = *pv <= *it; printf("++ %f <= %f = %d\n", *pv, *it, *itb ? 1 : 0); }
    std::vector<ssize_t> shape = { (ssize_t)nodes_values_.size(), values.size() };
    std::vector<ssize_t> strides = { (ssize_t)(values.size()*sizeof(int)),
                                     (ssize_t)sizeof(int) };
    return py::array_t<bool>(
        py::buffer_info(
            &result[0],
            sizeof(int),
            py::format_descriptor<int>::format(),
            2,
            shape,                                   /* shape of the matrix       */
            strides                                  /* strides for each axis     */
        ));
}


template<typename NTYPE>
py::array_t<NTYPE> RuntimeTreeEnsembleRegressor<NTYPE>::compute_tree_outputs(py::array_t<NTYPE> X) const {
    
    std::vector<int64_t> x_dims;
    arrayshape2vector(x_dims, X);
    if (x_dims.size() != 2)
        throw std::runtime_error("X must have 2 dimensions.");

    int64_t stride = x_dims.size() == 1 ? x_dims[0] : x_dims[1];  
    int64_t N = x_dims.size() == 1 ? 1 : x_dims[0];
    
    std::vector<NTYPE> result(N * roots_.size());
    const NTYPE* x_data = X.data(0);
    auto itb = result.begin();

    for (int64_t i=0; i < N; ++i)  //for each class
    {
        int64_t current_weight_0 = i * stride;
        for (size_t j = 0; j < roots_.size(); ++j, ++itb) {
            std::unordered_map<int64_t, std::tuple<NTYPE, NTYPE, NTYPE>> scores; // sum, min, max
            ProcessTreeNode(scores, roots_[j], x_data, current_weight_0);
            *itb = std::get<0>(scores[0]);
        }
    }
    
    std::vector<ssize_t> shape = { (ssize_t)N, (ssize_t)roots_.size() };
    std::vector<ssize_t> strides = { (ssize_t)(roots_.size()*sizeof(NTYPE)),
                                     (ssize_t)sizeof(NTYPE) };
    return py::array_t<bool>(
        py::buffer_info(
            &result[0],
            sizeof(NTYPE),
            py::format_descriptor<NTYPE>::format(),
            2,
            shape,                                   /* shape of the matrix       */
            strides                                  /* strides for each axis     */
        ));
}


class RuntimeTreeEnsembleRegressorFloat : public RuntimeTreeEnsembleRegressor<float>
{
    public:
        RuntimeTreeEnsembleRegressorFloat() : RuntimeTreeEnsembleRegressor<float>() {}
};


class RuntimeTreeEnsembleRegressorDouble : public RuntimeTreeEnsembleRegressor<double>
{
    public:
        RuntimeTreeEnsembleRegressorDouble() : RuntimeTreeEnsembleRegressor<double>() {}
};


#ifndef SKIP_PYTHON

PYBIND11_MODULE(op_tree_ensemble_regressor_, m) {
	m.doc() =
    #if defined(__APPLE__)
    "Implements runtime for operator TreeEnsembleRegressor."
    #else
    R"pbdoc(Implements runtime for operator TreeEnsembleRegressor. The code is inspired from
`tree_ensemble_regressor.cc <https://github.com/microsoft/onnxruntime/blob/master/onnxruntime/core/providers/cpu/ml/tree_ensemble_Regressor.cc>`_
in :epkg:`onnxruntime`.)pbdoc"
    #endif
    ;

    py::class_<RuntimeTreeEnsembleRegressorFloat> clf (m, "RuntimeTreeEnsembleRegressorFloat",
        R"pbdoc(Implements float runtime for operator TreeEnsembleRegressor. The code is inspired from
`tree_ensemble_regressor.cc <https://github.com/microsoft/onnxruntime/blob/master/onnxruntime/core/providers/cpu/ml/tree_ensemble_Regressor.cc>`_
in :epkg:`onnxruntime`. Supports float only.)pbdoc");

    clf.def(py::init<>());
    clf.def_readonly("roots_", &RuntimeTreeEnsembleRegressorFloat::roots_,
                     "Returns the roots indices.");
    clf.def("init", &RuntimeTreeEnsembleRegressorFloat::init,
            "Initializes the runtime with the ONNX attributes in alphabetical order.");
    clf.def("compute", &RuntimeTreeEnsembleRegressorFloat::compute,
            "Computes the predictions for the random forest.");
    clf.def("runtime_options", &RuntimeTreeEnsembleRegressorFloat::runtime_options,
            "Returns indications about how the runtime was compiled.");
    clf.def("omp_get_max_threads", &RuntimeTreeEnsembleRegressorFloat::omp_get_max_threads,
            "Returns omp_get_max_threads from openmp library.");

    clf.def_readonly("nodes_treeids_", &RuntimeTreeEnsembleRegressorFloat::nodes_treeids_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("nodes_nodeids_", &RuntimeTreeEnsembleRegressorFloat::nodes_nodeids_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("nodes_featureids_", &RuntimeTreeEnsembleRegressorFloat::nodes_featureids_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("nodes_values_", &RuntimeTreeEnsembleRegressorFloat::nodes_values_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("nodes_hitrates_", &RuntimeTreeEnsembleRegressorFloat::nodes_hitrates_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("nodes_modes_", &RuntimeTreeEnsembleRegressorFloat::nodes_modes_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("nodes_truenodeids_", &RuntimeTreeEnsembleRegressorFloat::nodes_truenodeids_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("nodes_falsenodeids_", &RuntimeTreeEnsembleRegressorFloat::nodes_falsenodeids_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("missing_tracks_true_", &RuntimeTreeEnsembleRegressorFloat::missing_tracks_true_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("target_nodeids_", &RuntimeTreeEnsembleRegressorFloat::target_nodeids_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("target_treeids_", &RuntimeTreeEnsembleRegressorFloat::target_treeids_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("target_ids_", &RuntimeTreeEnsembleRegressorFloat::target_ids_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("target_weights_", &RuntimeTreeEnsembleRegressorFloat::target_weights_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("base_values_", &RuntimeTreeEnsembleRegressorFloat::base_values_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("n_targets_", &RuntimeTreeEnsembleRegressorFloat::n_targets_, "See :ref:`lpyort-TreeEnsembleRegressor`.");
    clf.def_readonly("post_transform_", &RuntimeTreeEnsembleRegressorFloat::post_transform_, "See :ref:`lpyort-TreeEnsembleRegressor`.");

    clf.def("debug_threshold", &RuntimeTreeEnsembleRegressorFloat::debug_threshold,
        "Checks every features against every features against every threshold. Returns a matrix of boolean.");
    clf.def("compute_tree_outputs", &RuntimeTreeEnsembleRegressorFloat::compute_tree_outputs,
        "Computes every tree output.");
        

    py::class_<RuntimeTreeEnsembleRegressorDouble> cld (m, "RuntimeTreeEnsembleRegressorDouble",
        R"pbdoc(Implements double runtime for operator TreeEnsembleRegressor. The code is inspired from
`tree_ensemble_regressor.cc <https://github.com/microsoft/onnxruntime/blob/master/onnxruntime/core/providers/cpu/ml/tree_ensemble_Regressor.cc>`_
in :epkg:`onnxruntime`. Supports double only.)pbdoc");

    cld.def(py::init<>());
    cld.def_readonly("roots_", &RuntimeTreeEnsembleRegressorDouble::roots_,
                     "Returns the roots indices.");
    cld.def("init", &RuntimeTreeEnsembleRegressorDouble::init,
            "Initializes the runtime with the ONNX attributes in alphabetical order.");
    cld.def("compute", &RuntimeTreeEnsembleRegressorDouble::compute,
            "Computes the predictions for the random forest.");
    cld.def("runtime_options", &RuntimeTreeEnsembleRegressorDouble::runtime_options,
            "Returns indications about how the runtime was compiled.");
    cld.def("omp_get_max_threads", &RuntimeTreeEnsembleRegressorDouble::omp_get_max_threads,
            "Returns omp_get_max_threads from openmp library.");

    cld.def_readonly("nodes_treeids_", &RuntimeTreeEnsembleRegressorDouble::nodes_treeids_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("nodes_nodeids_", &RuntimeTreeEnsembleRegressorDouble::nodes_nodeids_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("nodes_featureids_", &RuntimeTreeEnsembleRegressorDouble::nodes_featureids_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("nodes_values_", &RuntimeTreeEnsembleRegressorDouble::nodes_values_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("nodes_hitrates_", &RuntimeTreeEnsembleRegressorDouble::nodes_hitrates_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("nodes_modes_", &RuntimeTreeEnsembleRegressorDouble::nodes_modes_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("nodes_truenodeids_", &RuntimeTreeEnsembleRegressorDouble::nodes_truenodeids_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("nodes_falsenodeids_", &RuntimeTreeEnsembleRegressorDouble::nodes_falsenodeids_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("missing_tracks_true_", &RuntimeTreeEnsembleRegressorDouble::missing_tracks_true_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("target_nodeids_", &RuntimeTreeEnsembleRegressorDouble::target_nodeids_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("target_treeids_", &RuntimeTreeEnsembleRegressorDouble::target_treeids_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("target_ids_", &RuntimeTreeEnsembleRegressorDouble::target_ids_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("target_weights_", &RuntimeTreeEnsembleRegressorDouble::target_weights_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("base_values_", &RuntimeTreeEnsembleRegressorDouble::base_values_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("n_targets_", &RuntimeTreeEnsembleRegressorDouble::n_targets_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    cld.def_readonly("post_transform_", &RuntimeTreeEnsembleRegressorDouble::post_transform_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    // cld.def_readonly("leafnode_data_", &RuntimeTreeEnsembleRegressorDouble::leafnode_data_, "See :ref:`lpyort-TreeEnsembleRegressorDouble`.");
    
    cld.def("debug_threshold", &RuntimeTreeEnsembleRegressorDouble::debug_threshold,
        "Checks every features against every features against every threshold. Returns a matrix of boolean.");
    cld.def("compute_tree_outputs", &RuntimeTreeEnsembleRegressorDouble::compute_tree_outputs,
        "Computes every tree output.");
}

#endif
