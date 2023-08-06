#include <vector>
#include <map>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <pybind11/iostream.h>
#include <pybind11/numpy.h>
#include <pybind11/buffer_info.h>

#include "uni10_type.h"
#include "../include/uni10_api/Qnum.h"
#include "../include/uni10_api/Bond.h"
#include "../include/uni10_api/Block.h"
#include "../include/uni10_api/Matrix.h"
#include "../include/uni10_api/UniTensor.h"
#include "../include/uni10_api/UniTensor_para.h"
#include "../include/uni10_api/Network.h"

#include "../include/uni10_api/linalg.h"
#include "../include/uni10_api/linalg_inplace.h"
#include "../include/uni10_api/hirnk_linalg.h"
#include "../include/uni10_api/hirnk_linalg_inplace.h"

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(pyuni10, m){
	// Version number
	m.attr("__version__") = "2.1.0";

	/*************************** Qnum **************************/
	// Parity/Z2 type
	py::enum_<uni10::parityType>(m, "parityType")
		.value("PRT_EVEN", uni10::PRT_EVEN)	//< parity/Z2 even
		.value("PRT_ODD", uni10::PRT_ODD)	//< parity/Z2 odd
		.export_values();
	// Fermion parity type
	py::enum_<uni10::parityFType>(m, "parityFType")
		.value("PRTF_EVEN", uni10::PRTF_EVEN)	//< fermion parity even
		.value("PRTF_ODD", uni10::PRTF_ODD)	//< fermion parity odd
		.export_values();

	// Class Qnum
	py::class_<uni10::Qnum>(m, "Qnum")
		// Construction
		.def(py::init<int, uni10::parityType>(),
			"U1"_a = 0, "prt"_a = uni10::PRT_EVEN)
		.def(py::init<uni10::parityFType, int, uni10::parityType>(),
			"prtF"_a, "U1"_a = 0, "prt"_a = uni10::PRT_EVEN)
		.def(py::init<const uni10::Qnum&>())
		// Private member accessing
		.def_property_readonly("m_U1", &uni10::Qnum::U1)
		.def_property_readonly("m_prt", &uni10::Qnum::prt)
		.def_property_readonly("m_prtF", &uni10::Qnum::prtF)
		.def_property_readonly_static("Fermionic", &uni10::Qnum::isFermionic)
		// Method
		.def("U1", &uni10::Qnum::U1)
		.def("prt", &uni10::Qnum::prt)
		.def("prtF", &uni10::Qnum::prtF)
		.def_static("isFermionic", &uni10::Qnum::isFermionic)
		.def("assign", (void(uni10::Qnum::*)(int, uni10::parityType))&uni10::Qnum::assign,
			"U1"_a = 0, "prt"_a = uni10::PRT_EVEN)
		.def("assign", (void(uni10::Qnum::*)(uni10::parityFType, int, uni10::parityType))&uni10::Qnum::assign,
			"prtF"_a, "U1"_a = 0, "prt"_a = uni10::PRT_EVEN)
		// Operator overloading
		.def(py::self * py::self)
		.def(-py::self)
		.def(py::self < py::self)
		.def(py::self <= py::self)
		.def(py::self == py::self)
		.def("__hash__", &uni10::Qnum::hash)
		.def("__repr__", [](const uni10::Qnum &q){
			py::scoped_ostream_redirect stream(
				std::cout, py::module::import("sys").attr("stdout"));
			std::cout << "(U1 = " << std::setprecision(2) << q.U1() << ", P = " << std::setprecision(1) << q.prt() << ", " << q.prtF() << ")";
			return "";
		});

	/*************************** Bond **************************/
	// Bond type
	py::enum_<uni10::bondType>(m, "bondType")
		.value("BD_IN", uni10::BD_IN)	//< incoming bond
		.value("BD_OUT", uni10::BD_OUT)	//< outcoming bond
		.export_values();

	// Class Bond
	py::class_<uni10::Bond>(m, "Bond")
		// Construction
		.def(py::init<uni10::bondType, size_t>(),
			"tp"_a, "dim"_a)
		.def(py::init<uni10::bondType, const std::vector<uni10::Qnum>&>(),
			"tp"_a, "qnums"_a)
		.def(py::init<const uni10::Bond&>(),
			"bd"_a)

		// Method
		.def("TypeId", &uni10::Bond::TypeId)
		.def("assign", (void(uni10::Bond::*)(uni10::bondType, size_t))&uni10::Bond::assign,
			"tp"_a, "dim"_a)
		.def("assign", (void(uni10::Bond::*)(uni10::bondType, const std::vector<uni10::Qnum>&))&uni10::Bond::assign,
			"tp"_a, "qnums"_a)
		.def("type", &uni10::Bond::type)
		.def("dim", &uni10::Bond::dim)
		.def("degeneracy", &uni10::Bond::degeneracy)
		.def("Qlist", &uni10::Bond::Qlist)
		.def("change", &uni10::Bond::change)
		.def("dummy_change", &uni10::Bond::dummy_change)
		.def("combine", &uni10::Bond::combine)
		.def("WithSymmetry", &uni10::Bond::WithSymmetry)

		// Operator overloading
		.def(py::self == py::self)
		.def("__repr__", [](const uni10::Bond &bd){
			py::scoped_ostream_redirect stream(
				std::cout, py::module::import("sys").attr("stdout"));
			if(bd.type() == uni10::BD_IN)
				std::cout << "IN : ";
			else
				std::cout << "OUT: ";
			std::map<uni10::Qnum, uni10_int> qnums = bd.degeneracy();
			for(std::map<uni10::Qnum, uni10_int>::iterator it = qnums.begin(); it != qnums.end(); it ++)
				std::cout << it->first << "|" << it->second << ", ";
			std::cout << "Dim = " << bd.dim() << std::endl;
			return "";
		});
	// Function
	m.def("combine", (uni10::Bond(*)(uni10::bondType, const std::vector<uni10::Bond>&))&uni10::combine,
		"tp"_a, "bds"_a);
	m.def("combine", (uni10::Bond(*)(const std::vector<uni10::Bond>&))&uni10::combine,
		"bds"_a);

	/************************ UniTensor ************************/
	// Contain type
	py::enum_<uni10::contain_type>(m, "contain_type")
	.value("no_sym", uni10::no_sym)
	.value("bs_sym", uni10::bs_sym)
	.value("fm_sym", uni10::fm_sym)
	.value("spar_sym", uni10::spar_sym)
	.export_values();

	// Class UniTensor(REAL)
	py::class_<uni10::UniTensor<uni10_double64>>(m, "UniTensorR")
	// Constructor
	.def(py::init<uni10_double64, const uni10::contain_type>(),
		"val"_a, "s"_a = uni10::no_sym)
	.def(py::init<const std::vector<uni10::Bond>&, const std::string&>(),
		"_bonds"_a = std::vector<uni10::Bond>(), "_name"_a = "")
	.def(py::init<const std::vector<uni10::Bond>&, std::vector<int>&, const std::string&>(),
		"_bonds"_a = std::vector<uni10::Bond>(), "labels"_a, "_name"_a = "")
	.def(py::init([](py::array_t<uni10_double64, py::array::c_style | py::array::forcecast> b){
		py::buffer_info info = b.request();

		if(info.ndim != 2)
			throw std::runtime_error("Incompatible array dimension!");

		uni10::Qnum q0(0);
		std::vector<uni10::Bond> bds;

		std::vector<uni10::Qnum> iqnums(info.shape[0], q0);
		std::vector<uni10::Qnum> oqnums(info.shape[1], q0);
		bds.push_back(uni10::Bond(uni10::BD_IN, iqnums));
		bds.push_back(uni10::Bond(uni10::BD_OUT, oqnums));

		auto T = new uni10::UniTensor<uni10_double64>(bds);
		auto mat = uni10::Matrix<uni10_double64>(info.shape[0], info.shape[1]);
		mat.SetElem((uni10_double64*)info.ptr);
		T->PutBlock(mat);
		return std::unique_ptr<uni10::UniTensor<uni10_double64>>(T);
	}))
	.def(py::init<const uni10::UniTensor<uni10_double64>&>(),
		"UniT"_a)
	.def(py::init<const std::string&>(),
		"fname"_a)

	// Method
	.def("Save", &uni10::UniTensor<uni10_double64>::Save,
		"fname"_a)
	.def("Load", &uni10::UniTensor<uni10_double64>::Load,
		"fname"_a)
#ifdef UNI_HDF5
	.def("H5Save", &uni10::UniTensor<uni10_double64>::H5Save,
		"fname"_a, "gname"_a, "Override"_a)
	.def("H5Load", &uni10::UniTensor<uni10_double64>::H5Load,
		"fname"_a, "gname"_a)
#endif
	.def("Zeros", (void(uni10::UniTensor<uni10_double64>::*)())&uni10::UniTensor<uni10_double64>::Zeros)
	.def("Zeros", (void(uni10::UniTensor<uni10_double64>::*)
		(const uni10::Qnum&))&uni10::UniTensor<uni10_double64>::Zeros,
		"qnum"_a)
	.def("Ones", (void(uni10::UniTensor<uni10_double64>::*)())&uni10::UniTensor<uni10_double64>::Ones)
	.def("Ones", (void(uni10::UniTensor<uni10_double64>::*)
		(const uni10::Qnum&))&uni10::UniTensor<uni10_double64>::Ones,
		"qnum"_a)
	.def("Identity", (void(uni10::UniTensor<uni10_double64>::*)())&uni10::UniTensor<uni10_double64>::Identity)
	.def("Identity", (void(uni10::UniTensor<uni10_double64>::*)
		(const uni10::Qnum&))&uni10::UniTensor<uni10_double64>::Identity,
		"qnum"_a)
	.def("Randomize", (void(uni10::UniTensor<uni10_double64>::*)
		(char, uni10_double64, uni10_double64, uni10_int64))&uni10::UniTensor<uni10_double64>::Randomize,
		"UorN"_a = 'U', "dn_mu"_a = -1, "up_var"_a = 1, "seed"_a = uni10_clock)
	.def("Randomize", (void(uni10::UniTensor<uni10_double64>::*)
		(const uni10::Qnum&, char, uni10_double64, uni10_double64, uni10_int64))&uni10::UniTensor<uni10_double64>::Randomize,
		"qnum"_a, "UorN"_a = 'U', "dn_mu"_a = -1, "up_var"_a = 1, "seed"_a = uni10_clock)
	.def("OrthoRand", (void(uni10::UniTensor<uni10_double64>::*)
		(char, uni10_double64, uni10_double64, uni10_int64))&uni10::UniTensor<uni10_double64>::OrthoRand,
		"UorN"_a = 'U', "dn_mu"_a = -1, "up_var"_a = 1, "seed"_a = uni10_clock)
	.def("OrthoRand", (void(uni10::UniTensor<uni10_double64>::*)
		(const uni10::Qnum&, char, uni10_double64, uni10_double64, uni10_int64))&uni10::UniTensor<uni10_double64>::OrthoRand,
		"qnum"_a, "UorN"_a = 'U', "dn_mu"_a = -1, "up_var"_a = 1, "seed"_a = uni10_clock)
	.def("label", [](uni10::UniTensor<uni10_double64> UniT){
		return UniT.label();
	})
	.def("label", [](uni10::UniTensor<uni10_double64> UniT, size_t idx){
		return UniT.label(idx);
	})
	.def("GetName", &uni10::UniTensor<uni10_double64>::GetName)
	.def("SetName", &uni10::UniTensor<uni10_double64>::SetName,
		"_name"_a)
	.def("BondNum", &uni10::UniTensor<uni10_double64>::BondNum)
	.def("InBondNum", &uni10::UniTensor<uni10_double64>::InBondNum)
	.def("bond", [](uni10::UniTensor<uni10_double64> UniT){
		return UniT.bond();
	})
	.def("bond", [](uni10::UniTensor<uni10_double64> UniT, uni10_uint64 idx){
		return UniT.bond(idx);
	}, "idx"_a)
	.def("ElemNum", &uni10::UniTensor<uni10_double64>::ElemNum)
	.def("TypeId", &uni10::UniTensor<uni10_double64>::TypeId)
	.def("BlockNum", &uni10::UniTensor<uni10_double64>::BlockNum)
	.def("SetLabel", (void(uni10::UniTensor<uni10_double64>::*)
		(const uni10_int, const uni10_uint64))&uni10::UniTensor<uni10_double64>::SetLabel,
		"newLabel"_a, "idx"_a)
	.def("SetLabel", (void(uni10::UniTensor<uni10_double64>::*)
		(const std::vector<uni10_int>&))&uni10::UniTensor<uni10_double64>::SetLabel,
		"newLabels"_a)
	.def("BlocksQnum", &uni10::UniTensor<uni10_double64>::BlocksQnum)
	.def("BlockQnum", &uni10::UniTensor<uni10_double64>::BlockQnum,
		"idx"_a)
	.def("SetElem", (void(uni10::UniTensor<uni10_double64>::*)
		(const std::vector<uni10_double64>&))&uni10::UniTensor<uni10_double64>::SetElem,
		"_elem"_a)
	.def("Assign", &uni10::UniTensor<uni10_double64>::Assign,
		"_bond"_a)
	.def("CombineBond", [](uni10::UniTensor<uni10_double64> UniT, const std::vector<uni10_int>& combined_labels){
		return UniT.CombineBond(combined_labels);
	}, "combined_labels"_a)
	.def("At", &uni10::UniTensor<uni10_double64>::At,
		"idxs"_a)
	.def("PrintDiagram", [](uni10::UniTensor<uni10_double64>& UniT){
		py::scoped_ostream_redirect stream(
			std::cout, py::module::import("sys").attr("stdout"));
		UniT.PrintDiagram();
	})
	.def("PrintRawElem", [](uni10::UniTensor<uni10_double64>& UniT, bool print){
		py::scoped_ostream_redirect stream(
			std::cout, py::module::import("sys").attr("stdout"));
		return UniT.PrintRawElem(print);
	}, "print"_a = true)
	.def("Profile", [](uni10::UniTensor<uni10_double64>& UniT, bool print){
		py::scoped_ostream_redirect stream(
			std::cout, py::module::import("sys").attr("stdout"));
		return UniT.Profile(print);
	}, "print"_a = true)
	.def("Clear", &uni10::UniTensor<uni10_double64>::Clear)

	// Numpy API
	.def("GetElem", [](uni10::UniTensor<uni10_double64>& UniT){
		return py::array(py::buffer_info(UniT.GetElem(), sizeof(uni10_double64),
					py::format_descriptor<uni10_double64>::format(),
					UniT.ElemNum()));
	})
	.def("GetRawElem", [](uni10::UniTensor<uni10_double64>& UniT){
		auto mat = UniT.GetRawElem();
		return py::array(py::buffer_info(mat.GetElem(), sizeof(uni10_double64),
					py::format_descriptor<uni10_double64>::format(),
					2, { mat.row(), mat.col() },
					{ sizeof(uni10_double64) * mat.col(), sizeof(uni10_double64) }));
	})
	.def("SetRawElem", [](uni10::UniTensor<uni10_double64>& UniT,
						  py::array_t<uni10_double64, py::array::c_style | py::array::forcecast> b){
		py::buffer_info info = b.request();

		if(info.ndim == 1){
			UniT.SetRawElem((uni10_double64*)info.ptr);
		}
		else if(info.ndim == 2){
			auto mat = uni10::Matrix<uni10_double64>(info.shape[0], info.shape[1]);
			mat.SetElem((uni10_double64*)info.ptr);

			UniT.SetRawElem(mat);
		}
		else
			throw std::runtime_error("Incompatible array dimension!");
	}, "blk"_a)
	.def("PutBlock", [](uni10::UniTensor<uni10_double64>& UniT,
						py::array_t<uni10_double64, py::array::c_style | py::array::forcecast> b){
		py::buffer_info info = b.request();

		if(info.ndim != 2)
			throw std::runtime_error("Incompatible array dimension!");
		auto mat = uni10::Matrix<uni10_double64>(info.shape[0], info.shape[1]);
		mat.SetElem((uni10_double64*)info.ptr);

		UniT.PutBlock(mat);
	}, "mat"_a)
	.def("PutBlock", [](uni10::UniTensor<uni10_double64>& UniT, uni10::Qnum& qnum,
						py::array_t<uni10_double64, py::array::c_style | py::array::forcecast> b){
		py::buffer_info info = b.request();
		if(info.ndim != 2)
			throw std::runtime_error("Incompatible array dimension!");
		auto mat = uni10::Matrix<uni10_double64>(info.shape[0], info.shape[1]);
		mat.SetElem((uni10_double64*)info.ptr);

		UniT.PutBlock(qnum, mat);
	}, "qnum"_a, "mat"_a)
	.def("GetBlocks", [](uni10::UniTensor<uni10_double64>& UniT){
		std::map<uni10::Qnum, uni10::Matrix<uni10_double64>> blks = UniT.GetBlocks();
		std::map<uni10::Qnum, uni10::Matrix<uni10_double64>>::iterator it = blks.begin();
		std::map<uni10::Qnum, py::array> py_blks;
		py::array py_array;
		for(; it != blks.end(); it ++){
			py_array = py::array(py::buffer_info(it->second.GetElem(), sizeof(uni10_double64),
						py::format_descriptor<uni10_double64>::format(),
						2, { it->second.row(), it->second.col() },
						{ sizeof(uni10_double64) * it->second.col(), sizeof(uni10_double64) }));
			py_blks.insert(std::pair<uni10::Qnum, py::array>(it->first, py_array));
		}
		return py_blks;
	})
	.def("GetBlock", [](uni10::UniTensor<uni10_double64>& UniT, bool diag){
		auto mat = UniT.GetBlock(diag);

		return py::array(py::buffer_info(mat.GetElem(), sizeof(uni10_double64),
					py::format_descriptor<uni10_double64>::format(),
					2, { mat.row(), mat.col() },
					{ sizeof(uni10_double64) * mat.col(), sizeof(uni10_double64) }));
	}, "diag"_a = false)
	.def("GetBlock", [](uni10::UniTensor<uni10_double64>& UniT, const uni10::Qnum qnum, bool diag){
		auto mat = UniT.GetBlock(qnum, diag);

		return py::array(py::buffer_info(mat.GetElem(), sizeof(uni10_double64),
					py::format_descriptor<uni10_double64>::format(),
					2, { mat.row(), mat.col() },
					{ sizeof(uni10_double64) * mat.col(), sizeof(uni10_double64) }));
	}, "qnum"_a, "diag"_a = false)

	// Operator overloading
	.def(py::self * uni10_double64())
	.def(py::self * uni10_complex128())
	.def(uni10_double64() * py::self)
	.def(uni10_complex128() * py::self)
	.def(py::self + py::self)
	.def(py::self + uni10::UniTensor<uni10_complex128>())
	.def(py::self - py ::self)
	// .def(py::self - uni10::UniTensor<uni10_complex128>())
	.def(py::self += py::self)
	.def(py::self -= py::self)
	.def(py::self *= uni10_double64())
	.def("__repr__", [](uni10::UniTensor<uni10_double64>& UniT){
			py::scoped_ostream_redirect stream(
				std::cout, py::module::import("sys").attr("stdout"));
			std::cout << UniT << std::endl;
			return "";
	});

	// Class UniTensor(COMPLEX)
	py::class_<uni10::UniTensor<uni10_complex128>>(m, "UniTensorC")
	// Constructor
	.def(py::init<uni10_complex128, const uni10::contain_type>(),
		"val"_a, "s"_a = uni10::no_sym)
	.def(py::init<const std::vector<uni10::Bond>&, const std::string&>(),
		"_bonds"_a = std::vector<uni10::Bond>(), "_name"_a = "")
	.def(py::init<const std::vector<uni10::Bond>&, std::vector<int>&, const std::string&>(),
		"_bonds"_a = std::vector<uni10::Bond>(), "labels"_a, "_name"_a = "")
	.def(py::init([](py::array_t<uni10_complex128, py::array::c_style | py::array::forcecast> b){
		py::buffer_info info = b.request();

		if(info.ndim != 2)
			throw std::runtime_error("Incompatible array dimension!");

		uni10::Qnum q0(0);
		std::vector<uni10::Bond> bds;

		std::vector<uni10::Qnum> iqnums(info.shape[0], q0);
		std::vector<uni10::Qnum> oqnums(info.shape[1], q0);
		bds.push_back(uni10::Bond(uni10::BD_IN, iqnums));
		bds.push_back(uni10::Bond(uni10::BD_OUT, oqnums));
		auto T = new uni10::UniTensor<uni10_complex128>(bds);

		auto mat = uni10::Matrix<uni10_complex128>(info.shape[0], info.shape[1]);
		mat.SetElem((uni10_complex128*)info.ptr);
		T->PutBlock(mat);
		return std::unique_ptr<uni10::UniTensor<uni10_complex128>>(T);
	}))
	.def(py::init<const uni10::UniTensor<uni10_complex128>&>(),
		"UniT"_a)
	.def(py::init<const std::string&>(),
		"fname"_a)

	// Method
	.def("Save", &uni10::UniTensor<uni10_complex128>::Save,
		"fname"_a)
	.def("Load", &uni10::UniTensor<uni10_complex128>::Load,
		"fname"_a)
#ifdef UNI_HDF5
	.def("H5Save", &uni10::UniTensor<uni10_complex128>::H5Save,
		"fname"_a, "gname"_a, "Override"_a)
	.def("H5Load", &uni10::UniTensor<uni10_complex128>::H5Load,
		"fname"_a, "gname"_a)
#endif
	.def("Zeros", (void(uni10::UniTensor<uni10_complex128>::*)())&uni10::UniTensor<uni10_complex128>::Zeros)
	.def("Zeros", (void(uni10::UniTensor<uni10_complex128>::*)
		(const uni10::Qnum&))&uni10::UniTensor<uni10_complex128>::Zeros,
		"qnum"_a)
	.def("Ones", (void(uni10::UniTensor<uni10_complex128>::*)())&uni10::UniTensor<uni10_complex128>::Ones)
	.def("Ones", (void(uni10::UniTensor<uni10_complex128>::*)
		(const uni10::Qnum&))&uni10::UniTensor<uni10_complex128>::Ones,
		"qnum"_a)
	.def("Identity", (void(uni10::UniTensor<uni10_complex128>::*)())&uni10::UniTensor<uni10_complex128>::Identity)
	.def("Identity", (void(uni10::UniTensor<uni10_complex128>::*)
		(const uni10::Qnum&))&uni10::UniTensor<uni10_complex128>::Identity,
		"qnum"_a)
	.def("Randomize", (void(uni10::UniTensor<uni10_complex128>::*)
		(char, uni10_double64, uni10_double64, uni10_int64))&uni10::UniTensor<uni10_complex128>::Randomize,
		"UorN"_a = 'U', "dn_mu"_a = -1, "up_var"_a = 1, "seed"_a = uni10_clock)
	.def("Randomize", (void(uni10::UniTensor<uni10_complex128>::*)
		(const uni10::Qnum&, char, uni10_double64, uni10_double64, uni10_int64))&uni10::UniTensor<uni10_complex128>::Randomize,
		"qnum"_a, "UorN"_a = 'U', "dn_mu"_a = -1, "up_var"_a = 1, "seed"_a = uni10_clock)
	.def("OrthoRand", (void(uni10::UniTensor<uni10_complex128>::*)
		(char, uni10_double64, uni10_double64, uni10_int64))&uni10::UniTensor<uni10_complex128>::OrthoRand,
		"UorN"_a = 'U', "dn_mu"_a = -1, "up_var"_a = 1, "seed"_a = uni10_clock)
	.def("OrthoRand", (void(uni10::UniTensor<uni10_complex128>::*)
		(const uni10::Qnum&, char, uni10_double64, uni10_double64, uni10_int64))&uni10::UniTensor<uni10_complex128>::OrthoRand,
		"qnum"_a, "UorN"_a = 'U', "dn_mu"_a = -1, "up_var"_a = 1, "seed"_a = uni10_clock)
	.def("label", [](uni10::UniTensor<uni10_complex128> UniT){
		return UniT.label();
	})
	.def("label", [](uni10::UniTensor<uni10_complex128> UniT, size_t idx){
		return UniT.label(idx);
	})
	.def("GetName", &uni10::UniTensor<uni10_complex128>::GetName)
	.def("SetName", &uni10::UniTensor<uni10_complex128>::SetName,
		"_name"_a)
	.def("BondNum", &uni10::UniTensor<uni10_complex128>::BondNum)
	.def("InBondNum", &uni10::UniTensor<uni10_complex128>::InBondNum)
	.def("bond", [](uni10::UniTensor<uni10_complex128> UniT){
		return UniT.bond();
	})
	.def("bond", [](uni10::UniTensor<uni10_complex128> UniT, uni10_uint64 idx){
		return UniT.bond(idx);
	}, "idx"_a)
	.def("ElemNum", &uni10::UniTensor<uni10_complex128>::ElemNum)
	.def("TypeId", &uni10::UniTensor<uni10_complex128>::TypeId)
	.def("BlockNum", &uni10::UniTensor<uni10_complex128>::BlockNum)
	.def("SetLabel", (void(uni10::UniTensor<uni10_complex128>::*)
		(const uni10_int, const uni10_uint64))&uni10::UniTensor<uni10_complex128>::SetLabel,
		"newLabel"_a, "idx"_a)
	.def("SetLabel", (void(uni10::UniTensor<uni10_complex128>::*)
		(const std::vector<uni10_int>&))&uni10::UniTensor<uni10_complex128>::SetLabel,
		"newLabels"_a)
	.def("BlocksQnum", &uni10::UniTensor<uni10_complex128>::BlocksQnum)
	.def("BlockQnum", &uni10::UniTensor<uni10_complex128>::BlockQnum,
		"idx"_a)
	.def("SetElem", (void(uni10::UniTensor<uni10_complex128>::*)
		(const std::vector<uni10_complex128>&))&uni10::UniTensor<uni10_complex128>::SetElem,
		"_elem"_a)
	.def("Assign", &uni10::UniTensor<uni10_complex128>::Assign,
		"_bond"_a)
	.def("CombineBond", [](uni10::UniTensor<uni10_complex128> UniT, const std::vector<uni10_int>& combined_labels){
		return UniT.CombineBond(combined_labels);
	}, "combined_labels"_a)
	.def("At", &uni10::UniTensor<uni10_complex128>::At,
		"idxs"_a)
	.def("PrintDiagram", [](uni10::UniTensor<uni10_complex128>& UniT){
		py::scoped_ostream_redirect stream(
			std::cout, py::module::import("sys").attr("stdout"));
		UniT.PrintDiagram();
	})
	.def("PrintRawElem", [](uni10::UniTensor<uni10_complex128>& UniT, bool print){
		py::scoped_ostream_redirect stream(
			std::cout, py::module::import("sys").attr("stdout"));
		return UniT.PrintRawElem(print);
	}, "print"_a = true)
	.def("Profile", [](uni10::UniTensor<uni10_complex128>& UniT, bool print){
		py::scoped_ostream_redirect stream(
			std::cout, py::module::import("sys").attr("stdout"));
		return UniT.Profile(print);
	}, "print"_a = true)
	.def("Clear", &uni10::UniTensor<uni10_complex128>::Clear)

	// Numpy API
	.def("GetElem", [](uni10::UniTensor<uni10_complex128>& UniT){
		return py::array(py::buffer_info(UniT.GetElem(), sizeof(uni10_complex128),
					py::format_descriptor<uni10_complex128>::format(),
					UniT.ElemNum()));
	})
	.def("GetRawElem", [](uni10::UniTensor<uni10_complex128>& UniT){
		auto mat = UniT.GetRawElem();
		return py::array(py::buffer_info(mat.GetElem(), sizeof(uni10_complex128),
					py::format_descriptor<uni10_complex128>::format(),
					2, { mat.row(), mat.col() },
					{ sizeof(uni10_complex128) * mat.col(), sizeof(uni10_complex128) }));
	})
	.def("SetRawElem", [](uni10::UniTensor<uni10_complex128>& UniT,
						  py::array_t<uni10_complex128, py::array::c_style | py::array::forcecast> b){
		py::buffer_info info = b.request();

		if(info.ndim == 1){
			UniT.SetRawElem((uni10_complex128*)info.ptr);
		}
		else if(info.ndim == 2){
			auto mat = uni10::Matrix<uni10_complex128>(info.shape[0], info.shape[1]);
			mat.SetElem((uni10_complex128*)info.ptr);

			UniT.SetRawElem(mat);
		}
		else
			throw std::runtime_error("Incompatible array dimension!");
	}, "blk"_a)
	.def("PutBlock", [](uni10::UniTensor<uni10_complex128>& UniT,
						py::array_t<uni10_complex128, py::array::c_style | py::array::forcecast> b){
		py::buffer_info info = b.request();
		if(info.ndim != 2)
			throw std::runtime_error("Incompatible array dimension!");
		auto mat = uni10::Matrix<uni10_complex128>(info.shape[0], info.shape[1]);
		mat.SetElem((uni10_complex128*)info.ptr);

		UniT.PutBlock(mat);
	}, "mat"_a)
	.def("PutBlock", [](uni10::UniTensor<uni10_complex128>& UniT, uni10::Qnum& qnum,
						py::array_t<uni10_complex128, py::array::c_style | py::array::forcecast> b){
		py::buffer_info info = b.request();
		if(info.ndim != 2)
			throw std::runtime_error("Incompatible array dimension!");
		auto mat = uni10::Matrix<uni10_complex128>(info.shape[0], info.shape[1]);
		mat.SetElem((uni10_complex128*)info.ptr);

		UniT.PutBlock(qnum, mat);
	}, "qnum"_a, "mat"_a)
	.def("GetBlocks", [](uni10::UniTensor<uni10_complex128>& UniT){
		std::map<uni10::Qnum, uni10::Matrix<uni10_complex128>> blks = UniT.GetBlocks();
		std::map<uni10::Qnum, uni10::Matrix<uni10_complex128>>::iterator it = blks.begin();
		std::map<uni10::Qnum, py::array> py_blks;
		py::array py_array;
		for(; it != blks.end(); it ++){
			py_array = py::array(py::buffer_info(it->second.GetElem(), sizeof(uni10_complex128),
						py::format_descriptor<uni10_complex128>::format(),
						2, { it->second.row(), it->second.col() },
						{ sizeof(uni10_complex128) * it->second.col(), sizeof(uni10_complex128) }));
			py_blks.insert(std::pair<uni10::Qnum, py::array>(it->first, py_array));
		}
		return py_blks;
	})
	.def("GetBlock", [](uni10::UniTensor<uni10_complex128>& UniT, bool diag){
		auto mat = UniT.GetBlock(diag);

		return py::array(py::buffer_info(mat.GetElem(), sizeof(uni10_complex128),
					py::format_descriptor<uni10_complex128>::format(),
					2, { mat.row(), mat.col() },
					{ sizeof(uni10_complex128) * mat.col(), sizeof(uni10_complex128) }));
	}, "diag"_a = false)
	.def("GetBlock", [](uni10::UniTensor<uni10_complex128>& UniT, const uni10::Qnum qnum, bool diag){
		auto mat = UniT.GetBlock(qnum, diag);

		return py::array(py::buffer_info(mat.GetElem(), sizeof(uni10_complex128),
					py::format_descriptor<uni10_complex128>::format(),
					2, { mat.row(), mat.col() },
					{ sizeof(uni10_complex128) * mat.col(), sizeof(uni10_complex128) }));
	}, "qnum"_a, "diag"_a = false)

	// Operator overloading
	.def(py::self * uni10_double64())
	.def(py::self * uni10_complex128())
	.def(uni10_double64() * py::self)
	.def(uni10_complex128() * py::self)
	.def(py::self + py::self)
	.def(py::self + uni10::UniTensor<uni10_double64>())
	.def(py::self - py::self)
	.def(py::self - uni10::UniTensor<uni10_double64>())
	.def(py::self += py::self)
	.def(py::self += uni10::UniTensor<uni10_double64>())
	.def(py::self -= py::self)
	.def(py::self -= uni10::UniTensor<uni10_double64>())
	.def(py::self *= uni10_double64())
	.def(py::self *= uni10_complex128())
	.def("__repr__", [](uni10::UniTensor<uni10_complex128>& UniT){
			py::scoped_ostream_redirect stream(
				std::cout, py::module::import("sys").attr("stdout"));
			std::cout << UniT << std::endl;
			return "";
	});

	// Linear algebra
	m.def("Contract", [](const uni10::UniTensor<uni10_double64>& Ta, const uni10::UniTensor<uni10_double64>& Tb){
		return Contract(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("Contract", [](const uni10::UniTensor<uni10_double64>& Ta, const uni10::UniTensor<uni10_complex128>& Tb){
		return Contract(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("Contract", [](const uni10::UniTensor<uni10_complex128>& Ta, const uni10::UniTensor<uni10_double64>& Tb){
		return Contract(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("Contract", [](const uni10::UniTensor<uni10_complex128>& Ta, const uni10::UniTensor<uni10_complex128>& Tb){
		return Contract(Ta, Tb);
	}, "Ta"_a, "Tb"_a);

	m.def("PseudoContract", [](const uni10::UniTensor<uni10_double64>& Ta, const uni10::UniTensor<uni10_double64>& Tb){
		return PseudoContract(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("PseudoContract", [](const uni10::UniTensor<uni10_double64>& Ta, const uni10::UniTensor<uni10_complex128>& Tb){
		return PseudoContract(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("PseudoContract", [](const uni10::UniTensor<uni10_complex128>& Ta, const uni10::UniTensor<uni10_double64>& Tb){
		return PseudoContract(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("PseudoContract", [](const uni10::UniTensor<uni10_complex128>& Ta, const uni10::UniTensor<uni10_complex128>& Tb){
		return PseudoContract(Ta, Tb);
	}, "Ta"_a, "Tb"_a);

	m.def("Transpose", [](const uni10::UniTensor<uni10_double64>& kten){
		return Transpose(kten);
	}, "kten"_a);
	m.def("Transpose", [](const uni10::UniTensor<uni10_complex128>& kten){
		return Transpose(kten);
	}, "kten"_a);

	m.def("Dagger", [](const uni10::UniTensor<uni10_double64>& kten){
		return Dagger(kten);
	}, "kten"_a);
	m.def("Dagger", [](const uni10::UniTensor<uni10_complex128>& kten){
		return Dagger(kten);
	}, "kten"_a);

	m.def("Conj", [](const uni10::UniTensor<uni10_double64>& kten){
		return Conj(kten);
	}, "kten"_a);
	m.def("Conj", [](const uni10::UniTensor<uni10_complex128>& kten){
		return Conj(kten);
	}, "kten"_a);

	m.def("Permute", [](uni10::UniTensor<uni10_double64>& T, const std::vector<uni10_int>& newLabels, uni10_int inBondNum){
		Permute(T, newLabels, inBondNum, uni10::INPLACE);
	}, "T"_a, "newLabels"_a, "inBondNum"_a);
	m.def("Permute", [](uni10::UniTensor<uni10_complex128>& T, const std::vector<uni10_int>& newLabels, uni10_int inBondNum){
		Permute(T, newLabels, inBondNum, uni10::INPLACE);
	}, "T"_a, "newLabels"_a, "inBondNum"_a);
	m.def("Permute", [](uni10::UniTensor<uni10_double64>& T, uni10_int inBondNum){
		Permute(T, inBondNum, uni10::INPLACE);
	}, "T"_a, "inBondNum"_a);
	m.def("Permute", [](uni10::UniTensor<uni10_complex128>& T, uni10_int inBondNum){
		Permute(T, inBondNum, uni10::INPLACE);
	}, "T"_a, "inBondNum"_a);

	m.def("PseudoPermute", [](const uni10::UniTensor<uni10_double64>& T, const std::vector<uni10_int>& newLabels,
							  uni10_int inBondNum){
		return PseudoPermute(T, newLabels, inBondNum);
	}, "T"_a, "newLabels"_a, "inBondNum"_a);
	m.def("PseudoPermute", [](const uni10::UniTensor<uni10_double64>& T, const std::vector<uni10_int>& newLabels,
							  uni10_int inBondNum){
		return PseudoPermute(T, newLabels, inBondNum);
	}, "T"_a, "newLabels"_a, "inBondNum"_a);
	m.def("PseudoPermute", [](const uni10::UniTensor<uni10_double64>& T, uni10_int rowBondNum){
		return PseudoPermute(T, rowBondNum);
	}, "T"_a, "rowBondNum"_a);
	m.def("PseudoPermute", [](const uni10::UniTensor<uni10_complex128>& T, uni10_int rowBondNum){
		return PseudoPermute(T, rowBondNum);
	}, "T"_a, "rowBondNum"_a);

	m.def("PartialTrace", [](const uni10::UniTensor<uni10_double64>& Tin, uni10_int la, uni10_int lb){
		return PartialTrace(Tin, la, lb);
	}, "Tin"_a, "la"_a, "lb"_a);
	m.def("PartialTrace", [](const uni10::UniTensor<uni10_complex128>& Tin, uni10_int la, uni10_int lb){
		return PartialTrace(Tin, la, lb);
	}, "Tin"_a, "la"_a, "lb"_a);

	m.def("Trace", [](const uni10::UniTensor<uni10_double64>& Tin){
		return Trace(Tin);
	}, "Tin"_a);
	m.def("Trace", [](const uni10::UniTensor<uni10_complex128>& Tin){
		return Trace(Tin);
	}, "Tin"_a);

	m.def("Hosvd", (void(*)(uni10::UniTensor<uni10_double64>&, uni10_int*, uni10_int*, uni10_uint64,
							std::vector<uni10::UniTensor<uni10_double64>>&, uni10::UniTensor<uni10_double64>&,
							std::vector<std::map<uni10::Qnum, uni10::Matrix<uni10_double64>>>&,
							uni10::UNI10_INPLACE))&uni10::Hosvd,
		"Tin"_a, "group_labels"_a, "groups"_a, "groupsSize"_a, "Us"_a, "S"_a, "Ls"_a, "on"_a);
	m.def("Hosvd", (void(*)(uni10::UniTensor<uni10_complex128>&, uni10_int*, uni10_int*, uni10_uint64,
							std::vector<uni10::UniTensor<uni10_complex128>>&, uni10::UniTensor<uni10_complex128>&,
							std::vector<std::map<uni10::Qnum, uni10::Matrix<uni10_complex128>>>&,
							uni10::UNI10_INPLACE))&uni10::Hosvd,
		"Tin"_a, "group_labels"_a, "groups"_a, "groupsSize"_a, "Us"_a, "S"_a, "Ls"_a, "on"_a);

	m.def("Hosvd", (void(*)(uni10::UniTensor<uni10_double64>&, uni10_int*, uni10_int*, uni10_uint64,
							std::vector<uni10::UniTensor<uni10_double64>>&, uni10::UniTensor<uni10_double64>&,
							std::vector<uni10::Matrix<uni10_double64>>&,
							uni10::UNI10_INPLACE))&uni10::Hosvd,
		"Tin"_a, "group_labels"_a, "groups"_a, "groupsSize"_a, "Us"_a, "S"_a, "Ls"_a, "on"_a);
	m.def("Hosvd", (void(*)(uni10::UniTensor<uni10_complex128>&, uni10_int*, uni10_int*, uni10_uint64,
							std::vector<uni10::UniTensor<uni10_complex128>>&, uni10::UniTensor<uni10_complex128>&,
							std::vector<uni10::Matrix<uni10_complex128>>&,
							uni10::UNI10_INPLACE))&uni10::Hosvd,
		"Tin"_a, "group_labels"_a, "groups"_a, "groupsSize"_a, "Us"_a, "S"_a, "Ls"_a, "on"_a);

	m.def("Otimes", [](const uni10::UniTensor<uni10_double64>& Ta, const uni10::UniTensor<uni10_double64>& Tb){
		return Otimes(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("Otimes", [](const uni10::UniTensor<uni10_double64>& Ta, const uni10::UniTensor<uni10_complex128>& Tb){
		return Otimes(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("Otimes", [](const uni10::UniTensor<uni10_complex128>& Ta, const uni10::UniTensor<uni10_double64>& Tb){
		return Otimes(Ta, Tb);
	}, "Ta"_a, "Tb"_a);
	m.def("Otimes", [](const uni10::UniTensor<uni10_complex128>& Ta, const uni10::UniTensor<uni10_complex128>& Tb){
		return Otimes(Ta, Tb);
	}, "Ta"_a, "Tb"_a);

	/************************** Network ************************/
	// Class Network
	py::class_<uni10::Network>(m, "Network")
	// Constructor
	.def(py::init<const std::string&>(),
		 "fname"_a)

	// Method
	.def("PreConstruct", &uni10::Network::PreConstruct,
		"force"_a = true)
	.def("PutTensor", (void(uni10::Network::*)
		(int, const uni10::UniTensor<uni10_double64>&, bool))&uni10::Network::PutTensor,
		"idx"_a, "UniT"_a, "force"_a = true)
	.def("PutTensor", (void(uni10::Network::*)
		(int, const uni10::UniTensor<uni10_complex128>&, bool))&uni10::Network::PutTensor,
		"idx"_a, "UniT"_a, "force"_a = true)
	.def("PutTensor", (void(uni10::Network::*)
		(const std::string&, const uni10::UniTensor<uni10_double64>&, bool))&uni10::Network::PutTensor,
		"name"_a, "UniT"_a, "force"_a = true)
	.def("PutTensor", (void(uni10::Network::*)
		(const std::string&, const uni10::UniTensor<uni10_complex128>&, bool))&uni10::Network::PutTensor,
		"name"_a, "UniT"_a, "force"_a = true)
	.def("PutTensorT", (void(uni10::Network::*)
		(int, const uni10::UniTensor<uni10_double64>&, bool))&uni10::Network::PutTensorT,
		"idx"_a, "UniT"_a, "force"_a = true)
	.def("PutTensorT", (void(uni10::Network::*)
		(int, const uni10::UniTensor<uni10_complex128>&, bool))&uni10::Network::PutTensorT,
		"idx"_a, "UniT"_a, "force"_a = true)
	.def("PutTensorT", (void(uni10::Network::*)
		(const std::string&, const uni10::UniTensor<uni10_double64>&, bool))&uni10::Network::PutTensorT,
		"name"_a, "UniT"_a, "force"_a = true)
	.def("PutTensorT", (void(uni10::Network::*)
		(const std::string&, const uni10::UniTensor<uni10_complex128>&, bool))&uni10::Network::PutTensorT,
		"name"_a, "UniT"_a, "force"_a = true)
	.def("PutTensorD", (void(uni10::Network::*)
		(int, const uni10::UniTensor<uni10_double64>&, bool))&uni10::Network::PutTensorD,
		"idx"_a, "UniT"_a, "force"_a = true)
	.def("PutTensorD", (void(uni10::Network::*)
		(int, const uni10::UniTensor<uni10_complex128>&, bool))&uni10::Network::PutTensorD,
		"idx"_a, "UniT"_a, "force"_a = true)
	.def("PutTensorD", (void(uni10::Network::*)
		(const std::string&, const uni10::UniTensor<uni10_double64>&, bool))&uni10::Network::PutTensorD,
		"name"_a, "UniT"_a, "force"_a = true)
	.def("PutTensorD", (void(uni10::Network::*)
		(const std::string&, const uni10::UniTensor<uni10_complex128>&, bool))&uni10::Network::PutTensorD,
		"name"_a, "UniT"_a, "force"_a = true)
	.def("Launch", (void(uni10::Network::*)
		(uni10::UniTensor<uni10_double64>&, const std::string&))&uni10::Network::Launch,
		"Tout"_a, "Tname"_a = "")
	.def("Launch", (void(uni10::Network::*)
		(uni10::UniTensor<uni10_complex128>&, const std::string&))&uni10::Network::Launch,
		"Tout"_a, "Tname"_a = "")
	.def("GetContractOrder", &uni10::Network::GetContractOrder)

	// Operator overloading
	.def("__repr__", [](const uni10::Network& net){
		py::scoped_ostream_redirect stream(
				std::cout, py::module::import("sys").attr("stdout"));
		//net.print_network();
		std::cout << net << std::endl;
		return "";
	});
}
