#ifndef DEFINES_H
#define DEFINES_H

//#pragma pack(1)  // data struct in memory alignement
#pragma pack(push, 1)

#include <stddef.h>
// for (u)int64_t event_number
#ifdef _MSC_VER
#if _MSC_VER >= 1600  // MSVC++ 10 (2010)
#include <stdint.h>
#else
#include "external/stdint.h"
#endif
#else
#include <stdint.h>
#endif

// structure to store the hits
typedef struct HitInfo{
  int64_t event_number;  // event number value
  uint32_t trigger_number;  // trigger number
  uint32_t trigger_time_stamp;  // trigger time stamp
  uint8_t relative_BCID;  // relative BCID value
  uint16_t LVL1ID;  // LVL1ID
  uint8_t column;  // column value
  uint16_t row;  // row value
  uint8_t tot;  // ToT value
  uint16_t BCID;  // absolute BCID value
  uint16_t TDC;  // TDC value (12-bit value)
  uint16_t TDC_time_stamp;  // TDC time stamp (8-bit or 16-bit value)
  uint8_t TDC_trigger_distance;  // TDC trigger distance (8-bit value)
  uint8_t trigger_status;  // event service records
  uint32_t service_record;  // event service records
  uint16_t event_status;  // event status value
} HitInfo;

// structure to store the hits with cluster info
typedef struct ClusterHitInfo{
  int64_t event_number;  // event number value
  uint32_t trigger_number;  // trigger number
  uint32_t trigger_time_stamp;  // trigger time stamp
  uint8_t relative_BCID;  // relative BCID value
  uint16_t LVL1ID;  // LVL1ID
  uint8_t column;  // column value
  uint16_t row;  // row value
  uint8_t tot;  // ToT value
  uint16_t BCID;  // absolute BCID value
  uint16_t TDC;  // TDC value (12-bit value)
  uint16_t TDC_time_stamp;  // TDC time stamp (8-bit or 16-bit value)
  uint8_t TDC_trigger_distance;  // TDC trigger distance (8-bit value)
  uint8_t trigger_status;  // event service records
  uint32_t service_record;  // event service records
  uint16_t event_status;  // event status value
  uint16_t cluster_id;  // the cluster id of the hit
  uint8_t is_seed;  // flag to mark seed pixel
  uint16_t cluster_size;  // the cluster size of the cluster belonging to the hit
  uint16_t n_cluster;  // the number of cluster in the event
} ClusterHitInfo;

// structure to store the cluster
typedef struct ClusterInfo{
  int64_t event_number;  // event number value
  uint16_t ID;  // the cluster id of the cluster
  uint16_t size;  // sum tot of all cluster hits
  uint16_t tot;  // sum tot of all cluster hits
  uint8_t seed_column;  // seed pixel column value
  uint16_t seed_row;  // seed pixel row value
  float mean_column;  // column value
  float mean_row;  // row value
  uint16_t event_status;  // event status value
} ClusterInfo;

// structure for the input meta data
typedef struct MetaInfo{
  uint32_t startIndex;  // start index for this read out
  uint32_t stopIndex;  // stop index for this read out (exclusive!)
  uint32_t length;  // number of data word in this read out
  double timeStamp;  // time stamp of the readout
  uint32_t errorCode;  // error code for the read out (0: no error)
} MetaInfo;

// structure for the input meta data V2
typedef struct MetaInfoV2{
  uint32_t startIndex;  // start index for this read out
  uint32_t stopIndex;  // stop index for this read out (exclusive!)
  uint32_t length;  // number of data word in this read out
  double startTimeStamp;  // start time stamp of the readout
  double stopTimeStamp;  // stop time stamp of the readout
  uint32_t errorCode;  // error code for the read out (0: no error)
} MetaInfoV2;

// structures for the output meta data
typedef struct MetaInfoOut{
  int64_t eventIndex;  // event number of the read out
  double timeStamp;  // time stamp of the readout
  uint32_t errorCode;  // error code for the read out (0: no error)
} MetaInfoOut;

typedef struct MetaWordInfoOut{
  int64_t eventIndex;  // event number
  uint32_t startWordIdex;  // start word index
  uint32_t stopWordIdex;  // stop word index
} MetaWordInfoOut;

// DUT and TLU defines
const uint32_t __BCIDCOUNTERSIZE_FEI4A=256;  // BCID counter for FEI4A has 8 bit
const uint32_t __BCIDCOUNTERSIZE_FEI4B=1024;  // BCID counter for FEI4B has 10 bit
const uint32_t __NSERVICERECORDS=32;  // number of different service records
const size_t __MAXARRAYSIZE=2000000;  // maximum buffer array size for the output hit array (has to be bigger than hits in one chunk)
const size_t __MAXHITBUFFERSIZE=4000000;  // maximum buffer array size for the hit buffer array (has to be bigger than hits in one event)

// event status codes
const uint32_t __N_EVENT_STATUS_BITS=16;  // number of event error codes
const uint32_t __NO_ERROR=0;  // no error
const uint32_t __HAS_SR=1;  // the event has service records
const uint32_t __NO_TRG_WORD=2;  // the event has no trigger word, only for self-triggered data taking and injection
const uint32_t __NON_CONST_LVL1ID=4;  // LVL1ID changes in one event, happens in self-triggered mode
const uint32_t __EVENT_INCOMPLETE=8;  // BCID not increasing by 1, most likely BCID missing (incomplete data transmission)
const uint32_t __UNKNOWN_WORD=16;  // event has unknown words
const uint32_t __BCID_JUMP=32;  // BCID jumps, but either LVL1ID is constant or data is externally triggered with trigger word or TDC word
const uint32_t __TRG_ERROR=64;  // a trigger error occurred
const uint32_t __TRUNC_EVENT=128;  // Event had to many hits (>__MAXHITBUFFERSIZE) or data headers and was truncated
const uint32_t __TDC_WORD=256;  // Event has a TDC word
const uint32_t __MORE_THAN_ONE_TDC_WORD=512;  // Event has more than one valid TDC word (event has more than one TDC word in normal use mode or event has more than one valid TDC word in TRG delay mode)
const uint32_t __TDC_OVERFLOW=1024;  // Event has TDC word indicating a TDC overflow (value overflow in normal use mode and +no in time TDC in TRG delay use mode)
const uint32_t __NO_HIT=2048;  // Events without any hit, useful for trigger number debugging
const uint32_t __OTHER_WORD=4096;  // Events with words not related to the FEI4 readout
const uint32_t __MORE_THAN_ONE_HIT=8192;  // Events with more than one hit
const uint32_t __TDC_INVALID=16384;  // Events with invalid TDC words

// trigger status codes
const uint32_t __N_TRIGGER_STATUS_BITS=8;  // number of trigger error codes
const uint32_t __TRG_NO_ERROR=0;  // no trigger error
const uint32_t __TRG_NUMBER_INC_ERROR=1;  // two consecutive triggern numbers are not increasing by exactly one (counter overflow case considered correctly)
const uint32_t __TRG_NUMBER_MORE_ONE=2;  // more than one trigger per event
const uint32_t __TRG_ERROR_TRG_ACCEPT=4;  // TLU error
const uint32_t __TRG_ERROR_LOW_TIMEOUT=8;  // TLU error

// Clusterizer definitions
const uint32_t __MAXBCID=256;  // maximum possible BCID window width, 16 for the FE, 256 in FE stop mode
const uint32_t __MAXTOTBINS=128;  // number of ToT bins for the cluster ToT histogram (in ToT = [0:31])
const uint32_t __MAXCHARGEBINS=4096;  // number of charge bins for the cluster charge histogram (in PlsrDAC)
const uint32_t __MAXCLUSTERHITSBINS=1024;  // number of for the cluster size (= #hits) histogram
const uint32_t __MAXPOSXBINS=1000;  // number of bins in x for the 2d hit position histogram
const uint32_t __MAXPOSYBINS=1000;  // number of bins in y for the 2d hit position histogram

const uint32_t __MAXHITTOT=15;

// FE definitions
const uint32_t RAW_DATA_MIN_COLUMN=1;
const uint32_t RAW_DATA_MAX_COLUMN=80;
const uint32_t RAW_DATA_MIN_ROW=1;
const uint32_t RAW_DATA_MAX_ROW=336;

// trigger word macros
#define TRIGGER_WORD_HEADER_MASK 0x80000000  // 1xxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx, 31bit trigger data
#define TRIGGER_DATA_MASK 0x7FFFFFFF  // trigger data (either trigger number or time stamp)
#define TRIGGER_NUMBER_COMBINED_MASK 0x0000FFFF  // trigger number when using TLU trigger format 2 (combined data)
#define TRIGGER_TIME_STAMP_COMBINED_MASK 0x7FFF0000  // trigger time stamp when using TLU trigger format 2 (combined data)
#define TRIGGER_WORD_MACRO(X) (((TRIGGER_WORD_HEADER_MASK & X) == TRIGGER_WORD_HEADER_MASK) ? true : false)  // true if data word is trigger word
#define TRIGGER_DATA_MACRO(X) (TRIGGER_DATA_MASK & X)  // calculates the 31bit trigger data (either trigger number or time stamp) from a trigger word
#define TRIGGER_NUMBER_COMBINED_MACRO(X) (TRIGGER_NUMBER_COMBINED_MASK & X)  // calculates the 16bit trigger number from a trigger word when using TLU trigger format 2 (combined data)
#define TRIGGER_TIME_STAMP_COMBINED_MACRO(X) ((TRIGGER_TIME_STAMP_COMBINED_MASK & X) >> 16)  // calculates the 15bit time stamp from a trigger word when using TLU trigger format 2 (combined data)

// TLU trigger data format
#define TRIGGER_FROMAT_TRIGGER_NUMBER 0  // 0: trigger word contains trigger counter
#define TRIGGER_FROMAT_TIME_STAMP 1  // 1: trigger word contains time stamp
#define TRIGGER_FROMAT_COMBINED 2  // 2: trigger word contains both, 2: 15bit time stamp and 16bit trigger number

// TDC macros
#define __N_TDC_VALUES 4096
#define __N_TDC_TRG_DIST_VALUES 256
#define TDC_HEADER 0x40000000  // 0100 xxxx xxxx xxxx xxxx xxxx xxxx xxxx, x may contain user data
#define TDC_HEADER_MASK 0xF0000000  // select TDC header, no one-hot header
#define TDC_VALUE_MASK 0x00000FFF  // TDC value, 12bit
#define TDC_TIME_STAMP_MASK 0x0FFFF000  // TDC time stamp (or running counter), 16bit
#define TDC_SHORT_TIME_STAMP_MASK 0x000FF000  // short TDC time stamp (or running counter) when in use with TDC trigger distance, 8bit
#define TDC_TRIG_DIST_MASK 0x0FF00000  // TDC trigger distance, delay between trigger leading edge and TDC leading edge, 8bit
#define TDC_WORD_MACRO(X) (((TDC_HEADER_MASK & X) == TDC_HEADER) ? true : false)
#define TDC_VALUE_MACRO(X) (TDC_VALUE_MASK & X)
#define TDC_TIME_STAMP_MACRO(X) ((TDC_TIME_STAMP_MASK & X) >> 12)
#define TDC_SHORT_TIME_STAMP_MACRO(X) ((TDC_SHORT_TIME_STAMP_MASK & X) >> 12)
#define TDC_TRIG_DIST_MACRO(X) ((TDC_TRIG_DIST_MASK & X) >> 20)

// Other word macros (for data not directly related to FEI4, another module writing to SRAM with one-hot header)
#define OTHER_WORD_HEADER_3 0x20000000  // 001x xxxx xxxx xxxx xxxx xxxx xxxx xxxx, x may contain user data
#define OTHER_WORD_MASK_3 0xE0000000  // select one-hot header
#define OTHER_WORD_HEADER_4 0x10000000  // 0001 xxxx xxxx xxxx xxxx xxxx xxxx xxxx, x may contain user data
#define OTHER_WORD_MASK_4 0xF0000000  // select one-hot header
#define OTHER_WORD_MACRO(X) ((((OTHER_WORD_MASK_3 & X) == OTHER_WORD_HEADER_3) | ((OTHER_WORD_MASK_4 & X) == OTHER_WORD_HEADER_4)) ? true : false)

// Data Header (DH)
#define DATA_HEADER 0x00E90000
#define DATA_HEADER_MASK 0xF0FF0000
#define DATA_HEADER_FLAG_MASK 0x00008000
#define DATA_HEADER_LV1ID_MASK 0x00007F00
#define DATA_HEADER_LV1ID_MASK_FEI4B 0x00007C00  // data format changed in fE-I4B. Upper LV1IDs comming in seperate SR.
#define DATA_HEADER_BCID_MASK 0x000000FF
#define DATA_HEADER_BCID_MASK_FEI4B 0x000003FF  // data format changed in FE-I4B due to increased counter size, See DATA_HEADER_LV1ID_MASK_FEI4B also.

#define DATA_HEADER_MACRO(X) ((DATA_HEADER_MASK & X) == DATA_HEADER ? true : false)
#define DATA_HEADER_FLAG_MACRO(X) ((DATA_HEADER_FLAG_MASK & X) >> 15)
#define DATA_HEADER_FLAG_SET_MACRO(X) ((DATA_HEADER_FLAG_MASK & X) == DATA_HEADER_FLAG_MASK ? true : false)
#define DATA_HEADER_LV1ID_MACRO(X) ((DATA_HEADER_LV1ID_MASK & X) >> 8)
#define DATA_HEADER_LV1ID_MACRO_FEI4B(X) ((DATA_HEADER_LV1ID_MASK_FEI4B & X) >> 10)  // data format changed in fE-I4B. Upper LV1IDs comming in seperate SR.
#define DATA_HEADER_BCID_MACRO(X) (DATA_HEADER_BCID_MASK & X)
#define DATA_HEADER_BCID_MACRO_FEI4B(X) (DATA_HEADER_BCID_MASK_FEI4B & X)  // data format changed in FE-I4B due to increased counter size, See DATA_HEADER_LV1ID_MASK_FEI4B also.

// Data Record (DR)
#define DATA_RECORD 0x00000000
#define DATA_RECORD_MASK 0xF0000000
#define DATA_RECORD_COLUMN_MASK 0x00FE0000
#define DATA_RECORD_ROW_MASK 0x0001FF00
#define DATA_RECORD_TOT1_MASK 0x000000F0
#define DATA_RECORD_TOT2_MASK 0x0000000F

#define DATA_RECORD_MIN_COLUMN (RAW_DATA_MIN_COLUMN << 17)
#define DATA_RECORD_MAX_COLUMN (RAW_DATA_MAX_COLUMN << 17)
#define DATA_RECORD_MIN_ROW (RAW_DATA_MIN_ROW << 8)
#define DATA_RECORD_MAX_ROW (RAW_DATA_MAX_ROW << 8)

#define DATA_RECORD_MACRO(X) (((DATA_RECORD_COLUMN_MASK & X) <= DATA_RECORD_MAX_COLUMN) && ((DATA_RECORD_COLUMN_MASK & X) >= DATA_RECORD_MIN_COLUMN) && ((DATA_RECORD_ROW_MASK & X) <= DATA_RECORD_MAX_ROW) && ((DATA_RECORD_ROW_MASK & X) >= DATA_RECORD_MIN_ROW) && ((DATA_RECORD_MASK & X) == DATA_RECORD) ? true : false)
#define DATA_RECORD_COLUMN1_MACRO(X) ((DATA_RECORD_COLUMN_MASK & X) >> 17)
#define DATA_RECORD_ROW1_MACRO(X) ((DATA_RECORD_ROW_MASK & X) >> 8)
#define DATA_RECORD_TOT1_MACRO(X) ((DATA_RECORD_TOT1_MASK & X) >> 4)
#define DATA_RECORD_COLUMN2_MACRO(X) ((DATA_RECORD_COLUMN_MASK & X) >> 17)
#define DATA_RECORD_ROW2_MACRO(X) (((DATA_RECORD_ROW_MASK & X) >> 8) + 1)
#define DATA_RECORD_TOT2_MACRO(X) (DATA_RECORD_TOT2_MASK & X)

// Address Record (AR)
#define ADDRESS_RECORD 0x00EA0000
#define ADDRESS_RECORD_MASK 0xF0FF0000
#define ADDRESS_RECORD_TYPE_MASK 0x00008000
#define ADDRESS_RECORD_ADDRESS_MASK 0x00007FFF

#define ADDRESS_RECORD_MACRO(X) ((ADDRESS_RECORD_MASK & X) == ADDRESS_RECORD ? true : false)
#define ADDRESS_RECORD_TYPE_MACRO(X) ((ADDRESS_RECORD_TYPE_MASK & X) >> 15)
#define ADDRESS_RECORD_TYPE_SET_MACRO(X) ((ADDRESS_RECORD_TYPE_MASK & X) == ADDRESS_RECORD_TYPE_MASK ? true : false)
#define ADDRESS_RECORD_ADDRESS_MACRO(X) (ADDRESS_RECORD_ADDRESS_MASK & X)

// Value Record (VR)
#define VALUE_RECORD 0x00EC0000
#define VALUE_RECORD_MASK 0xF0FF0000
#define VALUE_RECORD_VALUE_MASK 0x0000FFFF

#define VALUE_RECORD_MACRO(X) ((VALUE_RECORD_MASK & X) == VALUE_RECORD ? true : false)
#define VALUE_RECORD_VALUE_MACRO(X) (VALUE_RECORD_VALUE_MASK & X)

// Service Record (SR)
#define SERVICE_RECORD 0x00EF0000
#define SERVICE_RECORD_MASK 0xF0FF0000
#define SERVICE_RECORD_CODE_MASK 0x0000FC00
#define SERVICE_RECORD_COUNTER_MASK 0x000003FF

#define SERVICE_RECORD_MACRO(X) ((SERVICE_RECORD_MASK & X) == SERVICE_RECORD ? true : false)
#define SERVICE_RECORD_CODE_MACRO(X) ((SERVICE_RECORD_CODE_MASK & X) >> 10)
#define SERVICE_RECORD_COUNTER_MACRO(X) (SERVICE_RECORD_COUNTER_MASK & X)

// FEI4B: SR 14
#define SERVICE_RECORD_LV1ID_MASK_FEI4B 0x000003F8
#define SERVICE_RECORD_BCID_MASK_FEI4B 0x00000007
#define SERVICE_RECORD_LV1ID_MACRO_FEI4B(X) ((SERVICE_RECORD_LV1ID_MASK_FEI4B & X) >> 3)
#define SERVICE_RECORD_BCID_MACRO_FEI4B(X) (SERVICE_RECORD_BCID_MASK_FEI4B & X)
// FEI4B: SR 16
#define SERVICE_RECORD_TF_MASK_FEI4B 0x00000200
#define SERVICE_RECORD_ETC_MASK_FEI4B 0x000001F0
#define SERVICE_RECORD_L1REQ_MASK_FEI4B 0x0000000F
#define SERVICE_RECORD_TF_MACRO_FEI4B(X) ((SERVICE_RECORD_TF_MASK_FEI4B & X) >> 9)
#define SERVICE_RECORD_ETC_MACRO_FEI4B(X) ((SERVICE_RECORD_ETC_MASK_FEI4B & X) >> 4)
#define SERVICE_RECORD_L1REQ_MACRO_FEI4B(X) (SERVICE_RECORD_L1REQ_MASK_FEI4B & X)

#pragma pack(pop)  // pop needed to suppress VS C4103 compiler warning
#endif  // DEFINES_H
