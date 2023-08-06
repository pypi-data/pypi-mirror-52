/*
   @Author : Kai-Hsin Wu
   @Date   : 2017/06/30
   @Version: v1.0
   @ for C++ version < 11
   */

#include <iostream>
#include <iomanip>

#include "uni10_parser.hpp"
#include "uni10_error.h"

using namespace std;

string RemoveBlnk(string istr){

  if(istr.empty()){ istr.clear(); return istr;}
  while(istr.at(0)==' '){
    istr.erase(istr.begin(),istr.begin()+1);

    if(istr.empty()){ istr.clear(); return istr;}
  }

  while(istr.at(istr.size()-1)==' '){
    istr.erase(istr.end()-1,istr.end());
    if(istr.empty()){ istr.clear(); return istr;}
  }

  if(istr.find(" ") != std::string::npos){ istr.clear(); return istr;}

  return istr;

}


int Parser::TryRead(const string &rawkey,const std::string &reading_var_string){

  map<string,unsigned int>::iterator it = matcher.find(RemoveBlnk(rawkey));
  if(it == matcher.end()) return 0;
  unsigned int idx = it->second;

  string rhs = RemoveBlnk(reading_var_string);
  if(rhs.empty()) return 0;


  //checkType:
  if(keys[idx].pType == Integer_){
    int* tmp = (int*)keys[idx].pVal;
    *tmp = atol(rhs.c_str());
  }else if(keys[idx].pType == UnsignedInteger_){
    unsigned int* tmp = (unsigned int*)keys[idx].pVal;
    *tmp = atol(rhs.c_str());
  }else if(keys[idx].pType == LongInteger_){
    long* tmp = (long*)keys[idx].pVal;
    *tmp = atol(rhs.c_str());
  }else if(keys[idx].pType == UnsignedLongInteger_){
    unsigned long* tmp = (unsigned long*)keys[idx].pVal;
    *tmp = atol(rhs.c_str());
  }else if(keys[idx].pType == Float_){
    float* tmp = (float*)keys[idx].pVal;
    *tmp = atof(rhs.c_str());
  }else if(keys[idx].pType == Double_){
    double* tmp = (double*)keys[idx].pVal;
    *tmp = atof(rhs.c_str());
  }else if(keys[idx].pType == String_){
    string* tmp = (string*)keys[idx].pVal;
    *tmp = rhs;
  }else if(keys[idx].pType == LongLongInteger_){
    long long* tmp = (long long*)keys[idx].pVal;
    *tmp = atoll(rhs.c_str());
  }else{
    uni10_error_msg(true,"%s","[ERROR][Parser::TryRead] invalid Type.");


  }
  keys[idx].isRead = 1;
  return 1;

}

void Parser::Parse(const string &rc_fname){

  FILE * pFile;
  char line[256];//buffer
  char *tmp;
  string lhs,rhs;
  pFile = fopen(rc_fname.c_str() , "rb");

  ///chk exist
  if(pFile != NULL){
    ///loop line
    while(1){

      ///chk EOF & read line
      if(fgets(line,sizeof(line),pFile)==NULL) break;

      if(line[0]=='#') continue;

      ///get lhs(key)
      tmp = strtok(line,"=");
      lhs = string(tmp);
      if(tmp != NULL){
        ///get rhs(val)
        tmp = strtok(NULL,"=");
        if(tmp ==NULL ) continue;
        tmp = strtok(tmp,"\n");
        if(tmp == NULL) continue;
        rhs = string(tmp);

        ///tryread:
        TryRead(lhs,rhs);
      }
    }

    fclose(pFile);
  }else{

    uni10_error_msg(true,"%s","[ERROR][Parser::Parse] invalid .rc file");

  }
}

void Parser::PrintBinds(){

  cout << "====================\n";
  cout << "Total element bind: " << keys.size()<<endl;

  for(int i=0;i<(int)keys.size();i++){
    cout << keys[i].key << "\t isRead " << keys[i].isRead  << "\t Type: " << types_dict_[keys[i].pType]  << endl;
  }

}

void Parser::PrintVars(){

  cout << "===============================\n";
  cout << "Total element bind: " << keys.size() << endl;
  cout << "---------------------------------" << endl;
  string stat;

  for(int idx=0;idx<(int)keys.size();idx++){

    if(keys[idx].isRead==0){

      cout << setw(8) << left << keys[idx].key << " [** No Parsed **] " << endl;
      continue;
    }

    //checkType:
    if(keys[idx].pType == Integer_){
      int* tmp = (int*)keys[idx].pVal;
      cout << setw(8) << left << keys[idx].key << " = " <<  *tmp << endl;
    }else if(keys[idx].pType == UnsignedInteger_){
      unsigned int* tmp = (unsigned int*)keys[idx].pVal;
      cout << setw(8) << left << keys[idx].key << "\t = " <<  *tmp << endl;
    }else if(keys[idx].pType == LongInteger_){
      long* tmp = (long*)keys[idx].pVal;
      cout << setw(8) << left << keys[idx].key << "\t = " <<  *tmp << endl;
    }else if(keys[idx].pType == UnsignedLongInteger_){
      unsigned long* tmp = (unsigned long*)keys[idx].pVal;
      cout << setw(8) << left << keys[idx].key << "\t = " <<  *tmp << endl;
    }else if(keys[idx].pType == Float_){
      float* tmp = (float*)keys[idx].pVal;
      cout << setw(8) << left << keys[idx].key << "\t = " <<  *tmp << endl;
    }else if(keys[idx].pType ==  Double_){
      double* tmp = (double*)keys[idx].pVal;
      cout << setw(8) << left << keys[idx].key << "\t = " <<  *tmp << endl;
    }else if(keys[idx].pType == String_){
      string* tmp = (string*)keys[idx].pVal;
      cout << setw(8) << left << keys[idx].key << "\t = " <<  *tmp << endl;
    }else if(keys[idx].pType == LongLongInteger_){
      long long* tmp = (long long*)keys[idx].pVal;
      cout << setw(8) << left << keys[idx].key << "\t = " <<  *tmp << endl;
    }else{
      uni10_error_msg(true,"%s","[ERROR][Parser::PrintVars] invalid Type.");
    }

  }
  cout << "=================================\n";

}

void Parser::Remove(const std::string &key){
  map<std::string,unsigned int>::iterator it;
  it = matcher.find(key);
  if(it!=matcher.end()){
    unsigned int idx = it->second;
    keys.erase(keys.begin()+idx);
    matcher.erase(it);
  }

}
void Parser::CheckAll(){
  int ff =0;
  string msg = "";
  for(int i=0;i<(int)keys.size();i++)
  {

    if(keys[i].isRead==0){
      //cout << "[ERROR][Parser::Check_All] < "  << keys[i].key << " > No read." << endl;
      msg += "[ERROR][Parser::Check_All] < " + keys[i].key + " > No read.\n";
      ff = 1;
    }
  }
  if(ff) uni10_error_msg(true,"%s",msg.c_str());

}

void Parser::Bind(const std::string &key, int &var){
  matcher[key] = keys.size();
  RowElem tmp = {NULL,"",Integer_,0 } ;
  tmp.pVal = (void*)&var;
  tmp.key = key;
  keys.push_back(tmp);

}

void Parser::Bind(const std::string &key, float &var){
  matcher[key] = keys.size();
  RowElem tmp = {NULL,"",Float_,0 } ;
  tmp.pVal = (void*)&var;
  tmp.key = key;
  keys.push_back(tmp);
}

void Parser::Bind(const std::string &key, unsigned int &var){
  matcher[key] = keys.size();
  RowElem tmp = {NULL,"",UnsignedInteger_,0 } ;
  tmp.pVal = (void*)&var;
  tmp.key = key;
  keys.push_back(tmp);
}

void Parser::Bind(const std::string &key, unsigned long &var){
  matcher[key] = keys.size();
  RowElem tmp = {NULL,"",UnsignedLongInteger_,0 } ;
  tmp.pVal = (void*)&var;
  tmp.key = key;
  keys.push_back(tmp);
}

void Parser::Bind(const std::string &key, long &var){
  matcher[key] = keys.size();
  RowElem tmp = {NULL,"",LongInteger_,0 } ;
  tmp.pVal = (void*)&var;
  tmp.key = key;
  keys.push_back(tmp);
}

void Parser::Bind(const std::string &key, double &var){
  matcher[key] = keys.size();
  RowElem tmp = {NULL,"",Double_,0 } ;
  tmp.pVal = (void*)&var;
  tmp.key = key;
  keys.push_back(tmp);
}

void Parser::Bind(const std::string &key, std::string &var){
  matcher[key] = keys.size();
  RowElem tmp = {NULL,"",String_,0 } ;
  tmp.pVal = (void*)&var;
  tmp.key = key;
  keys.push_back(tmp);
}

void Parser::Bind(const std::string &key, long long &var){
  matcher[key] = keys.size();
  RowElem tmp = {NULL,"",LongLongInteger_,0 } ;
  tmp.pVal = (void*)&var;
  tmp.key = key;
  keys.push_back(tmp);
}
