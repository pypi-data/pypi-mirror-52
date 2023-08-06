#include <math.h>

#include "uni10_error.h"
#include "uni10_api/Matrix.h"

namespace uni10{

  template <> template <>
    void Matrix<uni10_complex128>::Init_(const UELEM(UniElem, _package, _type)<uni10_double64>& _m){

      this->elem_.Init(this->row_, this->col_, this->diag_, _m);

    };

  template <> template <>
    void Matrix<uni10_double64>::Init_(const UELEM(UniElem, _package, _type)<uni10_complex128>& _m){

      this->elem_.Init(this->row_, this->col_, this->diag_,_m);

    };

  // Copy constructor of RotC or CtoR.
  template<> template<>
    Matrix<uni10_complex128>::Matrix(Matrix<uni10_double64> const& _m): Block<uni10_complex128>(_m.row_, _m.col_, _m.diag_){

      this->Init_(_m.elem_);

    }

  template<> template<>
    Matrix<uni10_double64>::Matrix(Matrix<uni10_complex128> const& _m): Block<uni10_double64>(_m.row_, _m.col_, _m.diag_){

      this->Init_(_m.elem_);

    }

  template<> template<>
    Matrix<uni10_complex128>::Matrix(Block<uni10_double64> const& _b): Block<uni10_complex128>(_b.row_, _b.col_, _b.diag_){

      this->Init_(_b.elem_);

    }

  template<> template<>
    Matrix<uni10_double64>::Matrix(Block<uni10_complex128> const& _b): Block<uni10_double64>(_b.row_, _b.col_, _b.diag_){

      this->Init_(_b.elem_);

    }

  //
  // Assignment operator
  template<> template<>
    Matrix<uni10_double64>& Matrix<uni10_double64>::operator=(const Matrix<uni10_complex128>& _m){

      this->row_ = _m.row_;
      this->col_ = _m.col_;
      this->diag_ = _m.diag_;
      this->Init_(_m.elem_);
      return *this;

    }

  template<> template<>
    Matrix<uni10_complex128>& Matrix<uni10_complex128>::operator=(const Matrix<uni10_double64>& _m){

      this->row_ = _m.row_;
      this->col_ = _m.col_;
      this->diag_ = _m.diag_;
      this->Init_(_m.elem_);
      return *this;

    }

  template<> template<>
    Matrix<uni10_double64>& Matrix<uni10_double64>::operator=(const Block<uni10_complex128>& _b){

      this->row_ = _b.row_;
      this->col_ = _b.col_;
      this->diag_ = _b.diag_;
      this->Init_(_b.elem_);
      return *this;

    }

  template<> template<>
    Matrix<uni10_complex128>& Matrix<uni10_complex128>::operator=(const Block<uni10_double64>& _b){

      this->row_ = _b.row_;
      this->col_ = _b.col_;
      this->diag_ = _b.diag_;
      this->Init_(_b.elem_);
      return *this;

    }

  Matrix<uni10_complex128>& operator+=(Matrix<uni10_complex128>& _m1, const Matrix<uni10_double64>& _m2){
    linalg_unielem_internal::MatrixAdd(&_m1.elem_, &_m1.diag_, &_m2.elem_, &_m2.diag_, &_m2.row_, &_m2.col_ );
    _m1.diag_ = (_m1.diag_ && _m2.diag_);
    return _m1;
  }
  
  Matrix<uni10_complex128>& operator-=(Matrix<uni10_complex128>& _m1, const Matrix<uni10_double64>& _m2){
    linalg_unielem_internal::MatrixSub(&_m1.elem_, &_m1.diag_, &_m2.elem_, &_m2.diag_, &_m2.row_, &_m2.col_ );
    _m1.diag_ = (_m1.diag_ && _m2.diag_);
    return _m1;
  }
  
  Matrix<uni10_double64>& operator-=(Matrix<uni10_double64>& _m1, Matrix<uni10_complex128> a){
    uni10_error_msg(true, "%s", "Can't use Matrix<double>::operator*=(T ) as [T = std::complex<double>] ");
    return _m1;
  }

  Matrix<uni10_complex128>& operator*=(Matrix<uni10_complex128>& _m1, const Matrix<uni10_double64>& _m2){            
    linalg_unielem_internal::MatrixMul(&_m1.elem_, &_m1.diag_, &_m2.elem_, &_m2.diag_, &_m2.row_, &_m2.col_ );
    _m1.diag_ = (_m1.diag_ || _m2.diag_);
    return _m1;
  }

};

