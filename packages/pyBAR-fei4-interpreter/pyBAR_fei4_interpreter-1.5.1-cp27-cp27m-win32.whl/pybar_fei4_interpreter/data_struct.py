import numpy as np
import tables as tb


class MetaTable(tb.IsDescription):
    start_index = tb.UInt32Col(pos=0)
    stop_index = tb.UInt32Col(pos=1)
    length = tb.UInt32Col(pos=2)
    # https://github.com/PyTables/PyTables/issues/230
#    timestamp = tb.Time64Col(pos=3)
    timestamp = tb.Float64Col(pos=3)
    error = tb.UInt32Col(pos=4)


class MetaTableV2(tb.IsDescription):
    index_start = tb.UInt32Col(pos=0)
    index_stop = tb.UInt32Col(pos=1)
    data_length = tb.UInt32Col(pos=2)
    # https://github.com/PyTables/PyTables/issues/230
    timestamp_start = tb.Float64Col(pos=3)
    timestamp_stop = tb.Float64Col(pos=4)
    error = tb.UInt32Col(pos=5)


def generate_scan_parameter_description(scan_parameters):
    '''Generate scan parameter dictionary. This is the only way to dynamically create table with dictionary, cannot be done with tables.IsDescription

    Parameters
    ----------
    scan_parameters : list, tuple
        List of scan parameters names (strings).

    Returns
    -------
    table_description : dict
        Table description.

    Usage
    -----
    pytables.createTable(self.raw_data_file_h5.root, name = 'scan_parameters', description = generate_scan_parameter_description(['PlsrDAC']), title = 'scan_parameters', filters = filter_tables)
    '''
    table_description = np.dtype([(key, tb.Int32Col(pos=idx)) for idx, key in enumerate(scan_parameters)])
    return table_description


def generate_scan_configuration_description(scan_parameters):
    '''Generate scan parameter dictionary. This is the only way to dynamically create table with dictionary, cannot be done with tables.IsDescription

    Parameters
    ----------
    scan_parameters : list, tuple
        List of scan parameters names (strings).

    Returns
    -------
    table_description : dict
        Table description.

    Usage
    -----
    pytables.createTable(self.raw_data_file_h5.root, name = 'scan_parameters', description = generate_scan_configuration_description(['PlsrDAC']), title = 'scan_parameters', filters = filter_tables)
    '''
    table_description = np.dtype([(key, tb.StringCol(512, pos=idx)) for idx, key in enumerate(scan_parameters)])
    return table_description


class HitInfoTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    trigger_number = tb.UInt32Col(pos=1)
    trigger_time_stamp = tb.UInt32Col(pos=2)
    relative_BCID = tb.UInt8Col(pos=3)
    LVL1ID = tb.UInt16Col(pos=4)
    column = tb.UInt8Col(pos=5)
    row = tb.UInt16Col(pos=6)
    tot = tb.UInt8Col(pos=7)
    BCID = tb.UInt16Col(pos=8)
    TDC = tb.UInt16Col(pos=9)
    TDC_time_stamp = tb.UInt16Col(pos=10)
    TDC_trigger_distance = tb.UInt8Col(pos=11)
    trigger_status = tb.UInt8Col(pos=12)
    service_record = tb.UInt32Col(pos=13)
    event_status = tb.UInt16Col(pos=14)


class MetaInfoEventTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    time_stamp = tb.Float64Col(pos=1)
    error_code = tb.UInt32Col(pos=2)


class MetaInfoEventTableV2(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    timestamp_start = tb.Float64Col(pos=1)
    timestamp_stop = tb.Float64Col(pos=2)
    error_code = tb.UInt32Col(pos=3)


class MetaInfoWordTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    start_index = tb.UInt32Col(pos=1)
    stop_index = tb.UInt32Col(pos=2)


class ClusterHitInfoTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    trigger_number = tb.UInt32Col(pos=1)
    trigger_time_stamp = tb.UInt32Col(pos=2)
    relative_BCID = tb.UInt8Col(pos=3)
    LVL1ID = tb.UInt16Col(pos=4)
    column = tb.UInt8Col(pos=5)
    row = tb.UInt16Col(pos=6)
    tot = tb.UInt8Col(pos=7)
    BCID = tb.UInt16Col(pos=8)
    TDC = tb.UInt16Col(pos=9)
    TDC_time_stamp = tb.UInt16Col(pos=10)
    TDC_trigger_distance = tb.UInt8Col(pos=11)
    trigger_status = tb.UInt8Col(pos=12)
    service_record = tb.UInt32Col(pos=13)
    event_status = tb.UInt16Col(pos=14)
    cluster_id = tb.UInt16Col(pos=15)
    is_seed = tb.UInt8Col(pos=16)
    cluster_size = tb.UInt16Col(pos=17)
    n_cluster = tb.UInt16Col(pos=18)


class ClusterInfoTable(tb.IsDescription):
    event_number = tb.Int64Col(pos=0)
    id = tb.UInt16Col(pos=1)
    size = tb.UInt16Col(pos=2)
    tot = tb.UInt16Col(pos=3)
    seed_column = tb.UInt8Col(pos=4)
    seed_row = tb.UInt16Col(pos=5)
    mean_column = tb.Float32Col(pos=6)
    mean_row = tb.Float32Col(pos=7)
    event_status = tb.UInt16Col(pos=8)


class MeanThresholdCalibrationTable(tb.IsDescription):
    parameter_value = tb.Int32Col(pos=0)
    vthin_altfine = tb.UInt32Col(pos=1)
    vthin_altcoarse = tb.UInt32Col(pos=2)
    mean_threshold = tb.Float64Col(pos=3)
    threshold_rms = tb.Float64Col(pos=4)


class ThresholdCalibrationTable(tb.IsDescription):
    column = tb.UInt8Col(pos=0)
    row = tb.UInt16Col(pos=1)
    parameter_value = tb.Int32Col(pos=2)
    vthin_altfine = tb.UInt32Col(pos=3)
    vthin_altcoarse = tb.UInt32Col(pos=4)
    threshold = tb.Float64Col(pos=5)


class MeanThresholdTable(tb.IsDescription):
    parameter = tb.Int32Col(pos=0)
    vthin_altfine = tb.UInt32Col(pos=1)
    vthin_altcoarse = tb.UInt32Col(pos=2)
    mean_threshold = tb.Float64Col(pos=3)
    threshold_rms = tb.Float64Col(pos=4)


class ThresholdTable(tb.IsDescription):
    column = tb.UInt8Col(pos=0)
    row = tb.UInt16Col(pos=1)
    parameter = tb.Int32Col(pos=2)
    vthin_altfine = tb.UInt32Col(pos=3)
    vthin_altcoarse = tb.UInt32Col(pos=4)
    threshold = tb.Float64Col(pos=5)
