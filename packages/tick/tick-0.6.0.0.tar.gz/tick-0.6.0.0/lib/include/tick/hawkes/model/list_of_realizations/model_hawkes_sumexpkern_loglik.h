
#ifndef LIB_INCLUDE_TICK_HAWKES_MODEL_LIST_OF_REALIZATIONS_MODEL_HAWKES_SUMEXPKERN_LOGLIK_H_
#define LIB_INCLUDE_TICK_HAWKES_MODEL_LIST_OF_REALIZATIONS_MODEL_HAWKES_SUMEXPKERN_LOGLIK_H_

// License: BSD 3 clause

#include "tick/base/base.h"
#include "tick/hawkes/model/base/model_hawkes_loglik.h"
#include "tick/hawkes/model/model_hawkes_sumexpkern_loglik_single.h"

/** \class ModelHawkesSumExpKernLogLik
 * \brief Class for computing L2 Contrast function and gradient for Hawkes
 * processes with exponential kernels with fixed exponent (i.e.,
 * alpha*beta*e^{-beta t}, with fixed beta) on a list of realizations
 */
class DLL_PUBLIC ModelHawkesSumExpKernLogLik : public ModelHawkesLogLik {
  //! @brief Value of decays array for this model
  ArrayDouble decays;

 public:
  // This exists soley for cereal/swig
  ModelHawkesSumExpKernLogLik() : ModelHawkesSumExpKernLogLik(ArrayDouble(), 0) {}

  /**
   * @brief Constructor
   * \param decay : decay for this model (remember that decay is fixed!)
   * \param max_n_threads : number of cores to be used for multithreading. If
   * negative, the number of physical cores will be used
   */

  ModelHawkesSumExpKernLogLik(const ArrayDouble &decay,
                              const int max_n_threads = 1);

  ~ModelHawkesSumExpKernLogLik() {}

  //! @brief Returns decay that was set
  SArrayDoublePtr get_decays() const {
    ArrayDouble copied_decays = decays;
    return copied_decays.as_sarray_ptr();
  }

  /**
   * @brief Set new decays
   * \param decay : new decays
   * \note Weights will need to be recomputed
   */
  void set_decays(ArrayDouble &decays) {
    this->decays = decays;
    weights_computed = false;
  }

  ulong get_n_decays() const { return decays.size(); }

  std::unique_ptr<ModelHawkesLogLikSingle> build_model(
      const int n_threads) override {
    return std::unique_ptr<ModelHawkesSumExpKernLogLikSingle>(
        new ModelHawkesSumExpKernLogLikSingle(decays, n_threads));
  }

  ulong get_n_coeffs() const override;

  template <class Archive>
  void serialize(Archive &ar) {
    ar(cereal::make_nvp("ModelHawkesLogLik",
                        cereal::base_class<ModelHawkesLogLik>(this)));

    ar(CEREAL_NVP(decays));
  }

  BoolStrReport compare(const ModelHawkesSumExpKernLogLik &that, std::stringstream &ss) {
    ss << get_class_name() << std::endl;
    auto are_equal = ModelHawkesLogLik::compare(that, ss) &&
                     TICK_CMP_REPORT(ss, decays);
    return BoolStrReport(are_equal, ss.str());
  }
  BoolStrReport compare(const ModelHawkesSumExpKernLogLik &that) {
    std::stringstream ss;
    return compare(that, ss);
  }
  BoolStrReport operator==(const ModelHawkesSumExpKernLogLik &that) {
    return ModelHawkesSumExpKernLogLik::compare(that);
  }
};

CEREAL_SPECIALIZE_FOR_ALL_ARCHIVES(ModelHawkesSumExpKernLogLik,
                                   cereal::specialization::member_serialize)

CEREAL_REGISTER_TYPE(ModelHawkesSumExpKernLogLik)

#endif  // LIB_INCLUDE_TICK_HAWKES_MODEL_LIST_OF_REALIZATIONS_MODEL_HAWKES_SUMEXPKERN_LOGLIK_H_
