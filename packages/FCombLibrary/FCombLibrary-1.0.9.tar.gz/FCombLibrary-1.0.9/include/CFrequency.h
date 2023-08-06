
#ifndef _CFrequency_h_
#define _CFrequency_h_

#include <iostream>
using std::ostream;

//---
//--- CFrequency
//---

class CFrequency
{
 protected:

	int fnum;
    double freq;
	double ampl;

 public:

    //---
    //--- leerer Konstruktor, erzeugt CTimePoint mit den Werten (0,0)
    //---
    CFrequency() {
	  freq = 0.0;
	  fnum = 0;  
	  ampl = 0.0;
    }

    //---
    //--- Konstruktor, um CTimePoint mit entsprechenden Werten zu erzeugen
    //---
    CFrequency(int n, double f, double a) {
	  freq = f;
	  fnum = n;
	  ampl = a;
    }

    //---
    //--- Dekonstruktor
    //---
    ~CFrequency() { }

    //---
    //--- nach den Konstruktoren kommen jetzt die normalen Methoden die
    //--- jeder CFrequency hat:
    //---  

    int getNumber() const { return fnum; }
    void setNumber(int n) { fnum=n; }

    double getFrequency() const { return freq; }
    void setFrequency(double f) { freq=f; }

    double getAmplitude() const { return ampl; }
    void setAmplitude(double a) { ampl=a; }

};

//---
//--- Definition of operators for the comparison of CFrequencys
//---

int operator<(CFrequency const &t1, CFrequency const &t2) {
  return(t1.getFrequency()<t2.getFrequency());
}
int operator<=(CFrequency const &t1, CFrequency const &t2) {
  return(t1.getFrequency()<=t2.getFrequency());
}

#endif
