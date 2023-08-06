cimport numpy as cnp
cnp.import_array()  # if array is used it has to be imported, otherwise possible runtime error

cdef packed struct numpy_meta_word_data:
    cnp.int64_t event_number
    cnp.uint32_t start_word_index
    cnp.uint32_t stop__word_index

cdef packed struct numpy_meta_data:
    cnp.uint32_t start_index
    cnp.uint32_t stop_index
    cnp.uint32_t length
    cnp.float64_t timestamp
    cnp.uint32_t error

cdef packed struct numpy_meta_data_v2:
    cnp.uint32_t index_start
    cnp.uint32_t index_stop
    cnp.uint32_t data_length
    cnp.float64_t timestamp_start
    cnp.float64_t timestamp_stop
    cnp.uint32_t error

cdef packed struct numpy_par_info:
    cnp.int32_t scanParameter  # parameter setting

cdef packed struct numpy_hit_info:
    cnp.int64_t event_number  # event number value
    cnp.uint32_t trigger_number  # trigger number
    cnp.uint32_t trigger_time_stamp  # trigger time stamp
    cnp.uint8_t relative_BCID  # relative BCID value
    cnp.uint16_t LVL1ID  # LVL1ID
    cnp.uint8_t column  # column value
    cnp.uint16_t row  # row value
    cnp.uint8_t tot  # ToT value
    cnp.uint16_t BCID  # absolute BCID value
    cnp.uint16_t TDC  # TDC value (12-bit value)
    cnp.uint16_t TDC_time_stamp  # TDC time stamp (8-bit or 16-bit value)
    cnp.uint8_t TDC_trigger_distance  # TDC trigger distance (8-bit value)
    cnp.uint8_t trigger_status  # event trigger status
    cnp.uint32_t service_record  # event service records
    cnp.uint16_t event_status  # event status value

cdef packed struct numpy_cluster_hit_info:
    cnp.int64_t event_number  # event number value
    cnp.uint32_t trigger_number  # trigger number
    cnp.uint32_t trigger_time_stamp  # trigger time stamp
    cnp.uint8_t relative_BCID  # relative BCID value
    cnp.uint16_t LVL1ID  # LVL1ID
    cnp.uint8_t column  # column value
    cnp.uint16_t row  # row value
    cnp.uint8_t tot  # ToT value
    cnp.uint16_t BCID  # absolute BCID value
    cnp.uint16_t TDC  # TDC value (12-bit value)
    cnp.uint16_t TDC_time_stamp  # TDC time stamp (8-bit or 16-bit value)
    cnp.uint8_t TDC_trigger_distance  # TDC trigger distance (8-bit value)
    cnp.uint8_t trigger_status  # event trigger status
    cnp.uint32_t service_record  # event service records
    cnp.uint16_t event_status  # event status value
    cnp.uint16_t cluster_id  # the cluster id of the hit
    cnp.uint8_t is_seed  # flag to mark seed pixel
    cnp.uint16_t cluster_size  # the cluster id of the hit
    cnp.uint16_t n_cluster  # the cluster id of the hit

cdef packed struct numpy_cluster_info:
    cnp.int64_t event_number  # event number value
    cnp.uint16_t id  # the cluster id of the cluster
    cnp.uint16_t size  # sum ToT of all cluster hits
    cnp.uint16_t tot  # sum ToT of all cluster hits
    cnp.uint8_t seed_column  # column value
    cnp.uint16_t seed_row  # row value
    cnp.float32_t mean_column  # sum charge of all cluster hits
    cnp.float32_t mean_row  # sum charge of all cluster hits
    cnp.uint16_t event_status  # event status value
