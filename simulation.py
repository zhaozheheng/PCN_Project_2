# CS6352 project 2
# Zheheng Zhao
# zxz163930

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import rv
from event import Event, Kind
import heapq as pq

def simulation(lam):
    eList = []
    # for i in range(10):
    #     pq.heappush(eList, Event(rv.exp_rv(0.5), 0))

    # for i in range(10):
    #     print pq.heappop(eList).time

    pH = 0.4
    pL = 0.6
    mu1 = 20
    mu2H = 10
    mu2L = 50
    r2d = 0.25
    r21 = 0.25
    r22 = 0.5

    clock = 0.0

    NH1 = 0
    NH2 = 0
    NdepH1 = 0
    NdepH2 = 0
    EnH1 = 0.0
    EnH2 = 0.0

    NL1 = 0
    NL2 = 0
    NdepL1 = 0
    NdepL2 = 0
    EnL1 = 0.0
    EnL2 = 0.0

    Ndep = 0
    
    # set bool to control service status: busy or not
    ser1 = False
    ser2 = False

    pq.heappush(eList, Event(rv.exp_rv(lam), Kind.ARR))

    while(Ndep <= 500000):
        currEvent = pq.heappop(eList)
        prev = clock
        clock = currEvent.time

        # print NH1
        # print NL1
        # print NH2
        # print NL2
        # update expected numbers
        EnH1 += NH1 * (clock - prev)
        EnH2 += NH2 * (clock - prev)
        EnL1 += NL1 * (clock - prev)
        EnL2 += NL2 * (clock - prev)

        # deal with arrival
        if currEvent.kind is Kind.ARR:
            if rv.uni_rv() <= pH:   # high priority
                NH1 += 1
                if not ser1:
                    ser1 = True
                    pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1H))
            else:   # low priority
                NL1 += 1
                if not ser1:
                    if NH1 > 0:
                        ser1 = True
                        pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1H))
                    elif NL1 > 0:
                        ser1 = True
                        pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1L))
            pq.heappush(eList, Event(clock + rv.exp_rv(lam), Kind.ARR)) # generate another arrival
        # high priority depart queue 1
        elif currEvent.kind is Kind.DEP1H:
            NH1 -= 1
            NdepH1 += 1
            NH2 += 1
            ser1 = False
            
            if NH1 > 0:
                ser1 = True
                pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1H))
            elif NL1 > 0:
                ser1 = True
                pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1L))
            if not ser2:
                ser2 = True
                pq.heappush(eList, Event(clock + rv.exp_rv(mu2H), Kind.DEP2H))
        # low priority depart queue 1
        elif currEvent.kind is Kind.DEP1L:
            NL1 -= 1
            NdepL1 += 1
            NL2 += 1
            ser1 = False

            if not ser2:
                if NH2 > 0:
                    ser2 = True
                    pq.heappush(eList, Event(clock + rv.exp_rv(mu2H), Kind.DEP2H))  # if server 2 not busy, generate high priority depart
                elif NL2 > 0:
                    ser2 = True
                    pq.heappush(eList, Event(clock + rv.exp_rv(mu2L), Kind.DEP2L))  # if server 2 not busy, generate low priority depart

            if NH1 > 0:
                ser1 = True
                pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1H))   # if server 1 not busy, generate high priority depart
            elif NL1 > 0:
                ser1 = True
                pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1L))   # if server 1 not busy, generate low priority depart
        # high priority depart queue 2
        elif currEvent.kind is Kind.DEP2H:
            NH2 -= 1
            NdepH2 += 1
            Ndep += 1
            ser2 = False

            if NH2 > 0:
                ser2 = True
                pq.heappush(eList, Event(clock + rv.exp_rv(mu2H), Kind.DEP2H))  # if server 2 not busy, generate high priority depart
            elif NL2 > 0:
                ser2 = True
                pq.heappush(eList, Event(clock + rv.exp_rv(mu2L), Kind.DEP2L))  # if server 2 not busy, generate low priority depart
        # low priority depart queue 2
        elif currEvent.kind is Kind.DEP2L:
            NL2 -= 1
            NdepL2 += 1
            ser2 = False
            if rv.uni_rv() <= r2d:  # leave system
                Ndep += 1
            elif rv.uni_rv() <= r2d + r21:  # go to queue 1
                NL1 += 1
                if not ser1:
                    if NH1 > 0:
                        ser1 = True
                        pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1H)) # if server 1 not busy, generate high priority depart
                    elif NL1 > 0:
                        ser1 = True
                        pq.heappush(eList, Event(clock + rv.exp_rv(mu1), Kind.DEP1L))   # if server 1 not busy, generate low priority depart
            else:   # go to queue 2
                NL2 += 1
                if not ser2:
                    if NH2 > 0:
                        ser2 = True
                        pq.heappush(eList, Event(clock + rv.exp_rv(mu2H), Kind.DEP2H))  # if server 2 not busy, generate high priority depart
                    elif NL2 > 0:
                        ser2 = True
                        pq.heappush(eList, Event(clock + rv.exp_rv(mu2L), Kind.DEP2L))  # if server 2 not busy, generate low priority depart
    
    # theoretical value caculator
    theL2 = pL * lam / (1 - r21 - r22)
    theL1 = theL2 * (1 - r22)
    theH2 = pH * lam
    theH1 = theH2
    
    print "------ lambda = " + str(lam) + " ------"

    # print EnH1
    # print EnL1
    # print EnH2
    # print EnL2

    print "High-priority throughput of Queue1 (theoretical): " + str(theH1)
    print "Low-priority throughput of Queue1 (theoretical): " + str(theL1)
    print "High-priority throughput of Queue2 (theoretical): " + str(theH2)
    print "Low-priority throughput of Queue2 (theoretical): " + str(theL2)

    print "High-priority throughput of Queue1 (simulation): " + str(NdepH1 / clock)
    print "Low-priority throughput of Queue1 (simulation): " + str(NdepL1 / clock)
    print "High-priority throughput of Queue2 (simulation): " + str(NdepH2 / clock)
    print "Low-priority throughput of Queue2 (simulation): " + str(NdepL2 / clock)

    print "Expected number of High-priority customers in Queue1 (simulation): " + str(EnH1 / clock)
    print "Expected number of Low-priority customers in Queue1 (simulation): " + str(EnL1 / clock)
    print "Expected number of High-priority customers in Queue2 (simulation): " + str(EnH2 / clock)
    print "Expected number of Low-priority customers in Queue2 (simulation): " + str(EnL2 / clock)

    print "Average time a High-priority customer spent in Queue2 (simulation): " + str(EnH2 / NdepH2)
    print "Average time a Low-priority customer spent in Queue2 (simulation): " + str(EnL2 / NdepL2)

    return theH1, theL1, theH2, theL2, NdepH1 / clock, NdepL1 / clock, NdepH2 / clock, NdepL2 / clock, EnH1 / clock, EnL1 / clock, EnH2 / clock, EnL2 / clock, EnH2 / NdepH2, EnL2 / NdepL2

theH1list = np.zeros(10)
theL1list = np.zeros(10)
theH2list = np.zeros(10)
theL2list = np.zeros(10)

thrH1list = np.zeros(10)
thrL1list = np.zeros(10)
thrH2list = np.zeros(10)
thrL2list = np.zeros(10)

EnH1list = np.zeros(10)
EnL1list = np.zeros(10)
EnH2list = np.zeros(10)
EnL2list = np.zeros(10)

taoH2list = np.zeros(10)
taoL2list = np.zeros(10)

# plot setting
lamlist = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
for i in range(lamlist.size):
    theH1list[i], theL1list[i], theH2list[i], theL2list[i], thrH1list[i], thrL1list[i], thrH2list[i], thrL2list[i], EnH1list[i], EnL1list[i], EnH2list[i], EnL2list[i], taoH2list[i], taoL2list[i] = simulation(lamlist[i])

f = plt.figure()

params = {'legend.fontsize': 'xx-small',
          'figure.figsize': (10, 10),
         'axes.labelsize': 'x-small',
         'axes.titlesize':'x-small',
         'xtick.labelsize':'x-small',
         'ytick.labelsize':'x-small'}
pylab.rcParams.update(params)

plt.subplot(331)
plt.plot(lamlist, thrH1list, lamlist, theH1list)
plt.xticks(np.arange(0.0, 10.0, 1.0))
plt.yticks(np.arange(0.0, 5.0, 1.0))
plt.title('YH1: blue--sim red--the')
plt.grid(True)

plt.subplot(332)
plt.plot(lamlist, thrL1list, lamlist, theL1list)
plt.xticks(np.arange(0.0, 10.0, 1.0))
plt.yticks(np.arange(0.0, 12.5, 1.0))
plt.title('YL1: blue--sim red--the')
plt.grid(True)

plt.subplot(333)
plt.plot(lamlist, thrH2list, lamlist, theH2list)
plt.xticks(np.arange(0.0, 10.0, 1.0))
plt.yticks(np.arange(0.0, 5.0, 1.0))
plt.title('YH2: blue--sim red--the')
plt.grid(True)

plt.subplot(334)
plt.plot(lamlist, thrL2list, lamlist, theL2list)
plt.xticks(np.arange(0.0, 10.0, 1.0))
plt.yticks(np.arange(0.0, 50.0, 5.0))
plt.title('YL2: blue--sim red--the')
plt.grid(True)

plt.subplot(335)
plt.plot(lamlist, EnH1list, lamlist, EnL1list)
plt.xticks(np.arange(0.0, 10.0, 1.0))
plt.yticks(np.arange(0.0, 3.0, 0.5))
plt.title('En1: blue--high red--low')
plt.grid(True)

plt.subplot(336)
plt.plot(lamlist, EnH2list, lamlist, EnL2list)
plt.xticks(np.arange(0.0, 10.0, 1.0))
plt.yticks(np.arange(0.0, 150000.0, 20000.0))
plt.title('En2: blue--high red--low')
plt.grid(True)

plt.subplot(338)
plt.plot(lamlist, taoH2list, lamlist, taoL2list)
plt.xticks(np.arange(0.0, 10.0, 1.0))
plt.yticks(np.arange(0.0, 15000.0, 2000.0))
plt.title('tao2: blue--high red--low')
plt.grid(True)

# plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
#                     wspace=0.35)
plt.tight_layout()

plt.show()

# save result
f.savefig("result.pdf", bbox_inches = 'tight')