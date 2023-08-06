

#ifndef _CFrequencyComposition_h_
#define _CFrequencyComposition_h_

#include <iostream>
using std::ostream;

#include "CFrequency.h"



class CFrequencyCompositionComponent {

 public: 
  int factor;
  int number;

  CFrequencyCompositionComponent(int f=0, int n=0) {
	factor=f;
	number=n;
  }

  ~CFrequencyCompositionComponent() { }
};

int operator<(CFrequencyCompositionComponent const &t1, 
			  CFrequencyCompositionComponent const &t2) {
  return(t1.number<t2.number);
}
int operator<=(CFrequencyCompositionComponent const &t1, 
			   CFrequencyCompositionComponent const &t2) {
  return(t1.number<=t2.number);
}



//---
//--- CFrequencyComposition
//---

class CFrequencyComposition : public CFrequency
{

private:
  vector<CFrequency*> components;
  string compositionString;

  void decodeCompositionString(string composition) {
	// set references...
  }

public:

  double getOffset() {
	return 0.0;
  }

  string getCompositionString() {
	return compositionString;
  }

  static string sortCompositionString(string sss) {
	

	/*	vector<CFrequencyCompositionComponent> components;
	components.push_back(CFrequencyCompositionComponent(k, knum));
	components.push_back(CFrequencyCompositionComponent(l, lnum));
	components.push_back(CFrequencyCompositionComponent(m, mnum));

	sort(components.begin(), components.end());

	ostringstream ostr;
	ostr << ((components[0].factor<0)?"-":"")
		 << fabs(components[0].factor) 
		 << "f" << components[0].number << endl;
	for (int i=1; i<3; i++) {
	  ostr << ((components[i].factor<0)?"-":"+") 
		   << fabs(components[i].factor) 
		   << "f" << components[i].number << endl;
	}
	return ostr.str();*/
	return "";
  }

  static string formatCompositionString(string s) {
	size_t found = s.find("1f");
	while (found!=string::npos) {
	  s.replace(found,2,"f");
	  found = s.find("1f");
	}
	return s;
  }

public:
  CFrequencyComposition(int num, double fr, string composition) {
	freq = fr;
	fnum = num;
	compositionString = composition;
	decodeCompositionString(composition);
  }

};


#endif
