/*
   @Author : Kai-Hsin Wu
   @Date   : 2017/06/30
   @Version: v1.0
   @ for C++ version < 11
   */

#ifndef PARSER_HPP_INCLUDED
#define PARSER_HPP_INCLUDED
#include <map>
#include <string>
#include <fstream>
#include <vector>
#include <cstring>

class Parser{

  private:

    enum {
      Integer_,
      Float_,
      UnsignedInteger_,
      UnsignedLongInteger_,
      LongInteger_,
      Double_,
      String_,
      LongLongInteger_
    };

    std::map<unsigned int,std::string> types_dict_;

  public :

    struct RowElem{
      void* pVal;
      std::string key;
      int pType;
      bool isRead;
    };

    Parser(){
      Init();
    }

    void Init(){
      types_dict_[Integer_]             = "int";
      types_dict_[Float_]               = "float";
      types_dict_[UnsignedInteger_]     = "unsigned int";
      types_dict_[UnsignedLongInteger_] = "unsigned long";
      types_dict_[LongInteger_]         = "long";
      types_dict_[Double_]               = "double";
      types_dict_[String_]              = "string";
      types_dict_[LongLongInteger_]     = "long long";
    }

    std::map<std::string,unsigned int > matcher;
    std::vector< RowElem > keys;

    //template<class T>
    void Bind(const std::string &key, int &var);
    void Bind(const std::string &key, float &var);
    void Bind(const std::string &key, unsigned int &var);
    void Bind(const std::string &key, unsigned long &var);
    void Bind(const std::string &key, long &var);
    void Bind(const std::string &key, double &var);
    void Bind(const std::string &key, std::string &var);
    void Bind(const std::string &key, long long &var);

    ///Overload for different type:
    int TryRead(const std::string &raw_key,const std::string &read_in_var_string);
    void Parse(const std::string &rc_fname);
    void PrintBinds();
    void PrintVars();
    void Remove(const std::string &keys);
    void CheckAll();

};

#endif // SSE_HPP_INCLUDED
