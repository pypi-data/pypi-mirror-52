// ============================================================================
// Copyright Jean-Charles LAMBERT - 2008-2016
//           Centre de donneeS Astrophysiques de Marseille (CeSAM)
// e-mail:   Jean-Charles.Lambert@lam.fr
// address:  Aix Marseille Universite, CNRS, LAM
//           Laboratoire d'Astrophysique de Marseille
//           Pole de l'Etoile, site de Chateau-Gombert
//           38, rue Frederic Joliot-Curie
//           13388 Marseille cedex 13 France
//           CNRS UMR 7326
// ============================================================================
//
// How to implement a plugin for UNSIO
//
//  see snapshotgadgeth5.cc as example
//
//
//
// 1) derive a class from snaphotinterface.h
//
//    template <class T> class CSnapshotMy : public CSnapshotInterfaceIn<T> { .. }
//
// 2) in constructor
//    detect if file as input parameter can be open by your class
//    if yes, set this->valid=true
//    then put every components range to a CRV object (see storeComponents())
// 3) in nextFrame() method
//    check that time requested match time to the current file
//    if yes, update user_select object according to which particles are
//    present in the file (this->crv populated via storeComponents)
//    then getRangeSelect() will return later, in getData, indexes
//    first,last of the component in memory
//    user_select.setSelection(this->getSelectPart(),&this->crv);
//    if (this->select_part=="all") {    // if "all" selected
//       user_select.setCrv(this->crv);  // CRVselect must be components presents in file/
//     }
// 4) implement all getData() methods
//     this methods must be able to return global array if user select "all" particles
//     this is mandatory for global vectors (pos,mass,vel,acc,pot,id)
//
//     getRangeSelect(component,&nbody,&first,&last)
//    - return true if component belong to particles selected by user
//    - set nbody to #bodies for the component
//    - set first and last index of particles. It's useful to know where are particles
//      of this component in global vectors
//  5) adapt CSnapshotsim and CSnspashotlist to your class
// ============================================================================
#ifndef UNSENGINE_H
#define UNSENGINE_H
/**
	@author Jean-Charles Lambert <jean-charles.lambert@lam.fr>
*/

#include <cstring>
#include <string>
#include "snapshotinterface.h"
#include <map>
#include "version.h"

namespace uns {

const std::string VERSION=std::string(UNSIO_MAJOR)+"."+
                          std::string(UNSIO_MINOR)+"."+
                          std::string(UNSIO_PATCH)+
                          std::string(UNSIO_EXTRA); // UNSIO version

inline std::string getVersion() { return uns::VERSION; }

enum StringData {
      // data
      EMPTY     ,
      Time      ,
      Redshift  ,
      Pos       ,
      Vel       ,
      Mass      ,
      Id        ,
      Rho       ,
      Hsml      ,
      U         ,  // internal Energy
      Keys      ,
      Aux       ,
      Eps       ,
      Pot       ,
      Acc       ,
      Age       ,
      Temp      ,  // temperature
      Ne        ,  // Temperature ElectronAbundance
      Sfr       ,  // Star formation rate
      Nh        ,  // NeutralHydrogenAbundance
      Metal     ,  // total metal : gas+stars
      GasMetal  ,  // metal for gas
      StarsMetal,  // metal for stars
      Zs        ,
      ZSMT      ,
      Im        ,
      Cm        ,
      Czs       ,
      Czsmt     ,
      Ssl       ,

      // Header
      Header    ,

      // hydro data
      Hydro     ,  // hydro arrays (mainly for RAMSES)
      Nvarh     ,  // #hydros arrays

      // Nbodies  per component
      Nsel      ,
      Nbody     ,
      Ngas      ,
      Nhalo     ,
      Ndisk     ,
      Nbulge    ,
      Nstars    ,
      Nbndry    ,

      // Components
      Gas       ,
      Halo      ,
      Disk      ,
      Bulge     ,
      Stars     ,
      Bndry     ,
      All       ,

      GasMPV    ,
      HaloMPV   ,
      DiskMPV   ,
      BulgeMPV  ,
      StarsMPV  ,
      BndryMPV  ,

      // Extra data
      Extra
  };

  // class Cuns
  // manage Unified Nbody Snapshot Input operations

  template <class T> class CunsIn2 {
  public:
    // constructor for READING opertaions
    CunsIn2(const char * ,const char * , const char *, const bool verb=false );
    CunsIn2(const std::string ,const std::string,const std::string, const bool verb=false );
    ~CunsIn2();
    bool isValid() { return valid;}
    uns::CSnapshotInterfaceIn<T> * snapshot; // object to store data

    // Map to associate component with a type
    static std::map<std::string, int> s_mapCompInt;
    static void initMap() {
      // initialise some maps
      CunsIn2::s_mapCompInt["gas"        ] = 0;
      CunsIn2::s_mapCompInt["halo"       ] = 1;
      CunsIn2::s_mapCompInt["dm"         ] = 1;
      CunsIn2::s_mapCompInt["disk"       ] = 2;
      CunsIn2::s_mapCompInt["bulge"      ] = 3;
      CunsIn2::s_mapCompInt["stars"      ] = 4;
      CunsIn2::s_mapCompInt["bndry"      ] = 5;
      CunsIn2::s_mapCompInt["all"        ] =-1;
    }

    //
    // py wrapper
    //
    int nextFrame(const char *  _bits);
    // T
    bool getData(const std::string  comp,const std::string  prop,
                 unsigned int * size,T ** farray);
    bool getData(const std::string  prop,
                 unsigned int * size,T ** farray);
    bool getData(const std::string  prop,T * fvalue);

    // int
    bool getData(const std::string  comp,const std::string  prop,
                 unsigned int * size,int ** iarray);
    bool getData(const std::string  prop,
                 unsigned int * size,int ** iarray);
    bool getData(const std::string  prop,int * ivalue);


    // close
    bool close() {
      bool status=false;
      if (isValid() && snapshot) {
        status=snapshot->close();
      }
      return status;
    }
    //
    std::string getFileName() {
      std::string ret ="";
      if (isValid() && snapshot) {
        ret=snapshot->getFileName();
      }
      return ret;
    }
    std::string getFileStructure() {
      std::string ret ="";
      if (isValid() && snapshot) {
        ret=snapshot->getFileStructure();
      }
      return ret;
    }
    std::string getInterfaceType() {
      std::string ret ="";
      if (isValid() && snapshot) {
        ret=snapshot->getInterfaceType();
      }
      return ret;
    }

  private:
    void init(const std::string ,const std::string,const std::string, const bool verb=false );
    std::string simname, sel_comp, sel_time; // IN
    void tryGadget();
    void tryGadgetH5();
    void tryNemo();
    void trySimDB();
    void trySnapList();
    void tryRamses();

    //bool findSim();
    bool valid;
    bool verbose;
  };
typedef CunsIn2<float>  CunsIn;  // to preserve compatibility with unsio 1.X
typedef CunsIn2<float>  CunsInF;
typedef CunsIn2<double> CunsInD;

  // class CunsOut2
  // manage Unified Nbody Snapshot Output operations
  template <class T> class CunsOut2 {
  public:

    // constructor for WRITING operations
    CunsOut2(const std::string, const std::string, const bool verb=false);
    ~CunsOut2();
    bool isValid() { return valid;}
    uns::CSnapshotInterfaceOut<T> * snapshot; // object to store data


    // Map to associate the strings with the enum values
    static std::map<std::string, StringData> s_mapStringValues;

    // py wrapper
    // setData FLOAT/DOUBLE
    int setData(const std::string  comp,const std::string  prop,
                unsigned int  size,T * farray, const bool _addr=false);
    int setData(const std::string  prop,
                unsigned int  size,T * farray, const bool _addr=false);
    int setData(const std::string  prop,
                T fvalue);
    // setData INT
    int setData(const std::string  comp,const std::string  prop,
                unsigned int  size,int * iarray, const bool _addr=false);
    int setData(const std::string  prop,
                unsigned int  size,int * iarray, const bool _addr=false);
    int setData(const std::string  prop,
                int ivalue);

    //
    int save();
    // close
    bool close() {
      bool status=false;
      if (isValid() && snapshot) {
        status=snapshot->close();
      }
      return status;
    }
    // py wrapper

    static  void initializeStringMap(const bool);
  private:
    std::string simname, simtype;           // OUT

    //bool findSim();
    bool valid;
    bool verbose;
  };

typedef CunsOut2<float>  CunsOut;  // to preserve compatibility with unsio 1.X
typedef CunsOut2<float>  CunsOutF;
typedef CunsOut2<double> CunsOutD;
}

#endif
