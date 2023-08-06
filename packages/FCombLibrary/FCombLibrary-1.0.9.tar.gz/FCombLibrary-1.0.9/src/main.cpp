
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
#include "CFreqCombinations.h"


int main (int argc, char* argv[])
{

	vector <FData> vec;
    if (argc!=2) {
        cout<<"\n\tfreqcombiscanner"
            <<"\n\t\tsearches for combination frequencies"<<endl;
        cout<<"\n\tsynopsis:\n\t\t./freqcombiscanner <p04 freq file>\n"<< endl;
        return 1;
    }


    char  *file   =      argv[1];
    ifstream infile(file);
    if (!infile.is_open()) {
        cout << "Failed to open file " << file << endl;
        return 1;
    }


    double accuracy = 0.005;
    int combo_depth = 4;
    cout << "-------------------------------------------------" << endl;
    cout << "-         Frequency Combination Scanner         -" << endl;
    cout << "-------------------------------------------------" << endl;
    cout << "  Check the frequency resolution of your data!" << endl;
    cout << "  Maximum frequency difference: " << accuracy << endl;
    cout << "-------------------------------------------------" << endl;
    cout << "  Maximum factor  for harmonics = " << combo_depth
         << "\n     -''-        for kF1 +- lF2 = " << combo_depth-1
         << "\n     -''-     kF1 +- lf2 +- mF3 = " << combo_depth-2 << endl;
    cout << "-------------------------------------------------" << endl;
    cout << "  The best composition is determined based on\n"
         << "  the amplitudes of the components,\n"
         << "  probably improvement needed!" << endl;
    cout << "-------------------------------------------------" << endl;

    // read in first interesting line
    //
    CFreqArray      initArray;
    char line[256];
    infile.getline(line, 256);
    int cnt = 0;
    while (!infile.eof()) {
        double freq=-9999999, ampl=0.0;
        string dummy;
        int fnum;

        istringstream istr(line);
        istr >> dummy;
        if (!dummy.compare("#")) {
            infile.getline(line, 256);
            continue;
        }
        stringstream sint(dummy.substr(1,dummy.size()-1));
        sint >> fnum;
        istr >> freq;
        istr >> ampl;

        //cout << fnum << " " << freq << " " << ampl << endl;

        vec.push_back({fnum,freq,ampl});
        initArray.add( CFrequency(fnum,freq,ampl) );
        cout << "f" << fnum << "\t" << showpoint << (freq<0.0?"":" ")
             << freq << endl;

        infile.getline(line, 256);
        cnt +=1;
        if (cnt > 200)
            break;
    }
    for (int i = 0;i < initArray.entries();++i)
    {
        cout << "f " << initArray.entry(i)->Data.getFrequency() << endl;
    }

	get_combinations(vec,combo_depth,accuracy);
	mFreqArray.clean();
	initArray.clean();
	mFreqCompositionArray.clean();
    return 0;
}

