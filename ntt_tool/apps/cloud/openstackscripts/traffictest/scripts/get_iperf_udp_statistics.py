import json
import os
import re
import sys


fileid = sys.argv[1]
filedir = os.getcwd()


def get_list_of_filenames():
    file_list = []
    for file in os.listdir(filedir):
        if file.startswith("udptesttrafficclient") and file.endswith("%s.txt" % (fileid)):
            file_list.append(file)
    return file_list


def process_files(file_list):
    out = {}
    for file in file_list:
        out[file] = get_test_results(file)
    return out


def get_test_results(file):
    """
    For a given test output file, return a tuple of the following format
    (bandwidth_loss dict wth keys interval_time, transferred, bandwidth, 
     jitter, loss_datagram, total_datagram, loss_percent)
    """
    bandwidth_stats = \
        {'interval_time': '',   # NOQA
         'transferred': '',   # NOQA
         'bandwidth': '',   # NOQA
         'jitter': '',  # NOQA
         'loss_datagram': '',  # NOQA
         'total_datagram': '',  # NOQA
         'loss_percent': ''}

    reportflag = False
    f = open(file, 'r')

    for line in f:
        if "- - " in line:
            reportflag = True
        if "[ ID]" in line and reportflag:
            report = f.next()
            report_data = report.split(']')[1].split('  ')
            # also want packets transmitted, packets received, % packet loss
            datagram = report.split('/')[2]
            total_datagram = datagram.split('(')[0]
            loss_percent = datagram.split('(')[1].split('%')[0]
            if str(report_data[2]) == 'sec':
                interval_time =str(report_data[1]) + " " + str(report_data[2])
                loss_datagram = report_data[6].split('/')[0]
            else:
                interval_time =str(report_data[1])
                loss_datagram = report_data[5].split('/')[0]
            bandwidth_stats = \
                {'interval_time': interval_time,   # NOQA
                 'transferred': str(report_data[3]),   # NOQA
                 'bandwidth': str(report_data[4]),   # NOQA
                 'jitter': str(report_data[5]),  # NOQA
                 'loss_datagram': str(loss_datagram),  # NOQA
                 'total_datagram': str(total_datagram),  # NOQA
                 'loss_percent': str(loss_percent)}
    
    test_results = {'bandwidth_stats': bandwidth_stats}

    return test_results


def main():
    file_list = get_list_of_filenames()
    script_output = process_files(file_list)
    json_output = json.JSONEncoder().encode(script_output)
    # sample output
    # {'test.txt': ({'packet_loss': '0%'},
    #               {'rtt_min': '4.3', 'rtt_avg': '5.5', 'rtt_max': '6.3'})}
    print json_output

if __name__ == '__main__':
    main()
