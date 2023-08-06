
#include <iostream>
using std::cout;
using std::endl;
using std::flush;
using std::showpoint;  // to show trailing zeros
using std::left;

#include <tuple>
using std::pair;

#include <list>
using std::list;

#include <vector>
using std::vector;

#include <iomanip>
using std::setw;  // to show trailing string whitespace

#include <fstream>
using std::ifstream;
using std::ofstream;

#include <sstream>
using std::istringstream;
using std::ostringstream;
using std::stringstream;

#include <vector>
using std::vector;

#include <string>
using std::string;

#include <math.h>

#include "CFrequency.h"
#include "CFrequencyComposition.h"
#include "CLists.h"

class FData
{
public:
    FData()
    {
    };
    FData(int f_num,double freq, double ampl):
    f_num(f_num),
    freq(freq),
    ampl(ampl)
    {
    };
    int f_num;
    double freq;
    double ampl;
};

typedef TSortUpList<CFrequency> CFreqArray;
typedef CFrequency* SelectedFreq;

CFreqArray      mFreqArray;
CFreqArray      mFreqCompositionArray;

bool showdetails = false;




int getNum(double freq) {
    int size = mFreqArray.entries();
    mFreqArray.startiterate(0);
    for (int i=0; i<size; i++) {
        SelectedFreq tmp = mFreqArray.iterate();
        if (tmp->getFrequency()==freq)
            return tmp->getNumber();
    }
    return -1;
}

int getAmpl(double freq) {
    int size = mFreqArray.entries();
    mFreqArray.startiterate(0);
    for (int i=0; i<size; i++) {
        SelectedFreq tmp = mFreqArray.iterate();
        if (tmp->getFrequency()==freq)
            return tmp->getAmplitude();
    }
    return -1;
}

CFrequencyComposition checkForComposition(int fnum, double freq, double ampl, int maxdepth, double accuracy) {

    int depth = maxdepth;

    // maybe there are different posibilities:
    vector<string> compositionstrings;
    // check harmonics
    mFreqArray.startiterate(0);
    int size = mFreqArray.entries();
    for (int i=0; i<size; i++) {
        SelectedFreq tmp = mFreqArray.iterate();
        double f1 = tmp->getFrequency();
        for (int k=1; k<=depth; k++) {
            double diff = fabs(k*f1 - freq);
            if (diff < accuracy) {
                ostringstream ostr;
                ostr << "f" << fnum << "=" << k << "f" << tmp->getNumber()
                     << " " << diff
                     << " " << 0.01*pow(tmp->getAmplitude(),k)
                     << " " << ampl/pow(tmp->getAmplitude(),k);
                if (showdetails)
                    cout << "-> " << ostr.str() << endl;
                compositionstrings.push_back(ostr.str());
            }
        }
    }

    // copy into vector to check for other compositions
    vector<double> vfreqs;
    mFreqArray.startiterate(0);
    for (int i=0; i<size; i++) {
        SelectedFreq tmp = mFreqArray.iterate();
        vfreqs.push_back(tmp->getFrequency());
    }

    // check two-component compositions
    depth--; // reduce depth
    for (int i=0; i<size; i++) {
        //	for (int j=i+1; j<size; j++) {
        // we need 0 for - combinations, so we have duplicates for + combis
        for (int j=0; j<size; j++) {
            if (i==j)
                continue;
            // i and j define the frequency indices
            // k and l define the depth of the combination
            for (int k=1; k<=depth; k++) {
                for (int l=1; l<=depth; l++) {
                    double diff = fabs(k*vfreqs[i] + l*vfreqs[j] - freq);
                    if (diff < accuracy) {
                        ostringstream ostr;
                        ostr << "f" << fnum
                             << "=" << k << "f" << getNum(vfreqs[i])
                             << "+" << l << "f" << getNum(vfreqs[j])
                             << " " << diff
                             << " " << pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(0.01,k+l)
                             << " " << ampl/(pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l));
                        if (showdetails)
                            cout << "-> " << ostr.str() << endl;
                        compositionstrings.push_back(ostr.str());
                    }

                    diff = fabs(k*vfreqs[i] - l*vfreqs[j] - freq);
                    if (diff < accuracy) {
                        ostringstream ostr;
                        ostr << "f" << fnum
                             << "=" << k << "f" << getNum(vfreqs[i])
                             << "-" << l << "f" << getNum(vfreqs[j])
                             << " " << diff
                             << " " << pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(0.01,k+l)
                             << " " << ampl/(pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l));
                        if (showdetails)
                            cout << "-> " << ostr.str() << endl;
                        compositionstrings.push_back(ostr.str());
                    }
                }
            }
        }
    }

    // check three-component compositions
    depth--; // reduce depth
    for (int i=0; i<size; i++) {
        //for (int j=i+1; j<size; j++) {
        // we need 0 for - combinations, so we have duplicates for + combis
        for (int j=0; j<size; j++) {
            //for (int h=j+1; h<size; h++) {
            for (int h=0; h<size; h++) {
                if (i==j || j==h || i==h)
                    continue;
                // i,j and h define the frequency indices
                // k,l and m define the depth of the combination
                for (int k=1; k<=depth; k++) {
                    for (int l=1; l<=depth; l++) {
                        for (int m=1; m<=depth; m++) {
                            double diff = fabs(k*vfreqs[i] + l*vfreqs[j] + m*vfreqs[h] - freq);
                            if (diff < accuracy) {
                                ostringstream ostr;
                                ostr << "f" << fnum;
                                ostr << "=" << k << "f" << getNum(vfreqs[i])
                                     << "+" << l << "f" << getNum(vfreqs[j])
                                     << "+" << m << "f" << getNum(vfreqs[h])
                                     << " " << diff
                                     << " " << pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(getAmpl(vfreqs[h]),m)*pow(0.01,k+l+m)
                                     << " " << ampl/(pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(getAmpl(vfreqs[h]),m));
                                if (showdetails)
                                    cout << "-> " << ostr.str() << endl;
                                compositionstrings.push_back(ostr.str());
                            }
                            diff = fabs(k*vfreqs[i] + l*vfreqs[j] - m*vfreqs[h] - freq);
                            if (diff < accuracy) {
                                ostringstream ostr;
                                ostr << "f" << fnum
                                     << "=" << k << "f" << getNum(vfreqs[i])
                                     << "+" << l << "f" << getNum(vfreqs[j])
                                     << "-" << m << "f" << getNum(vfreqs[h])
                                     << " " << diff
                                     << " " << pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(getAmpl(vfreqs[h]),m)*pow(0.01,k+l+m)
                                     << " " << ampl/(pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(getAmpl(vfreqs[h]),m));
                                if (showdetails)
                                    cout << "-> " << ostr.str() << endl;
                                compositionstrings.push_back(ostr.str());
                            }
                            diff = fabs(k*vfreqs[i] - l*vfreqs[j] + m*vfreqs[h] - freq);
                            if (diff < accuracy) {
                                ostringstream ostr;
                                ostr << "f" << fnum
                                     << "=" << k << "f" << getNum(vfreqs[i])
                                     << "-" << l << "f" << getNum(vfreqs[j])
                                     << "+" << m << "f" << getNum(vfreqs[h])
                                     << " " << diff
                                     << " " << pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(getAmpl(vfreqs[h]),m)*pow(0.01,k+l+m)
                                     << " " << ampl/(pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(getAmpl(vfreqs[h]),m));
                                if (showdetails)
                                    cout << "-> " << ostr.str() << endl;
                                compositionstrings.push_back(ostr.str());
                            }
                            diff = fabs(k*vfreqs[i] - l*vfreqs[j] - m*vfreqs[h] - freq);
                            if (diff < accuracy) {
                                ostringstream ostr;
                                ostr << "f" << fnum
                                     << "=" << k << "f" << getNum(vfreqs[i])
                                     << "-" << l << "f" << getNum(vfreqs[j])
                                     << "-" << m << "f" << getNum(vfreqs[h])
                                     << " " << diff
                                     << " " << pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(getAmpl(vfreqs[h]),m)*pow(0.01,k+l+m)
                                     << " " << ampl/(pow(getAmpl(vfreqs[i]),k)*pow(getAmpl(vfreqs[j]),l)*pow(getAmpl(vfreqs[h]),m));
                                if (showdetails)
                                    cout << "-> " << ostr.str() << endl;
                                compositionstrings.push_back(ostr.str());
                            }
                        }
                    }
                }
            }
        }
    }

    // select the simplest composition
    string scompo="";
    string full = "";
    double weight=-1.0;
    double offset=-1.0;
    double mufactor=-1.0;
    sort(compositionstrings.begin(), compositionstrings.end());
    for (int i=0; i<compositionstrings.size(); i++) {
        string sc; double df=0.0; double iw=0.0, mu=0.0;
        istringstream istr(compositionstrings[i]);
        istr >> sc;
        istr >> df;
        istr >> iw;
        istr >> mu;
        full.append(";");
        full.append(sc);
        if (showdetails)
            cout << sc << " " << df << " " << iw << " " << iw/df << endl;
        //if (iw>weight && mu>0.0) { // this would be very strict!
        if (iw>weight) {
            weight=iw;
            scompo=sc;
            offset=df;
            mufactor=mu;
        }
    }
    scompo.append(full);
    return CFrequencyComposition(fnum, freq, scompo);
}

std::pair<std::list<string>,std::list<string> > get_combinations(vector <FData> vec,
                                                                 int combo_depth,
                                                                 double accuracy)
{
    std::list<string> comp_strings = {};
    std::list<string> independent_strings = {};

    for (int i=0; i<vec.size(); i++)
    {
        FData data = vec[i];
        CFrequencyComposition compo = checkForComposition(data.f_num ,data.freq,data.ampl
                ,combo_depth, accuracy);
        if (compo.getCompositionString().size()>0) {
            // add to composition array
            mFreqCompositionArray.add( compo );
            string s = compo.getCompositionString();
            comp_strings.push_back(s);

        } else {
            mFreqArray.add( CFrequency(data.f_num ,data.freq,data.ampl) );
            ostringstream ostr;
            ostr << "f" << data.f_num;
            independent_strings.push_back(ostr.str());
        }
    }

    std::pair<std::list<string>,std::list<string> > pair(comp_strings,independent_strings);
    return pair;
}
