#!/usr/bin/python

import socket
import calendar
import time

gtime = calendar.timegm(time.gmtime())

livestatus_path = "/var/cache/naemon/live"

livestatus_s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
livestatus_s.connect(livestatus_path)

livestatus_s.send("GET servicegroups\nColumns: name num_services num_services_hard_ok num_services_hard_warn num_services_hard_crit num_services_hard_unknown\n")

livestatus_s.shutdown(socket.SHUT_WR)

ls_answer = livestatus_s.recv(100000000)

result = []
for naeline in ls_answer[:-1].split('\n'):
    field = naeline.split(';')
    result.append("naemon.problems.servicegroups." + str(field[0]) + ".all " + str(field[1]) + " " + str(gtime) + "\n")
    result.append("naemon.problems.servicegroups." + str(field[0]) + ".ok " + str(field[2]) + " " + str(gtime) + "\n")
    result.append("naemon.problems.servicegroups." + str(field[0]) + ".warning " + str(field[3]) + " " + str(gtime) + "\n")
    result.append("naemon.problems.servicegroups." + str(field[0]) + ".critical " + str(field[4]) + " " + str(gtime) + "\n")
    result.append("naemon.problems.servicegroups." + str(field[0]) + ".unknown " + str(field[5]) + " " + str(gtime) + "\n")

carbon_s = socket.socket()
carbon_s.connect(('127.0.0.1',2003))

for metric in result:
    carbon_s.sendall(metric)

carbon_s.close
