#! /usr/bin/env python

import sys
import scikits.audiolab

def w(what):
    sys.stdout.write(what)

#t_file = 'audio.t.wav'
#z_file = 'audio.z.wav'

#t_signal, t_sample_frequency, t_encoding = scikits.audiolab.wavread(t_file)
#z_signal, z_sample_frequency, z_encoding = scikits.audiolab.wavread(z_file)

#print 'len t signal:', len(t_signal)
#print 'len z signal:', len(z_signal)

#bits = []
#for i in range(len(t_signal)):
#    t_bit = t_signal[i]
#    z_bit = z_signal[i]
#    bit = t_bit - z_bit
#    if abs(bit) >  0.1:
#        bits.append(i)

#print bits
#print len(bits), 'out of', len(t_signal), 'are different'

all_signals = []
for na in range(1,6):

    filename = 'a' * na + '.wav'
    filename = 'audiomanolo.wav'

    signals, sample_frequency, encoding = scikits.audiolab.wavread(filename)

#    print 'len signal:', len(signals)

    baudot_sample_frecuency = 45.45
    group_by = int(sample_frequency / baudot_sample_frecuency)

    print 'sample frecuency:', sample_frequency
    print 'baudot sample frecuency:', baudot_sample_frecuency
    print 'group by:', group_by

    all_signals.append(signals)
#    print 'signals:'
#    for s in signals[0:10]:
#        w(str(s) + ' ')
#    w('\n')

    all_changes = []
    read_signals = 0
    current = -2
    changes = 0
    for s in signals:
        if abs(s) > 0.1:
            if current < 0 and s > 0:
                current = 2
                changes += 1
            elif current > 0 and s <0:
                current = -2
                changes += 1
                
        read_signals += 1
        if read_signals % group_by == 0:
            all_changes.append(changes)
            current = -2
            changes = 0


    max_changes = max(all_changes)
    min_changes = min(x for x in all_changes if x != 0)
    print 'we have', len(all_changes)
    print 'all:', all_changes
    print 'max:', max_changes
    print 'min:', min_changes
    print len(all_changes) / baudot_sample_frecuency, 'seconds'
    
    print '__________________________________________________\n'

    bits = []
    for change in all_changes:
        if abs(max_changes - change) < abs(min_changes - change):
            bits.append(1)
        else:
            bits.append(0)
    print bits


    #import matplotlib.pyplot as plt
    #plt.plot(signals)
    #plt.ylabel('some numbers')
    #plt.show()

#max_len = max(len(signals) for signals in all_signals)
#print 'max length:', max_len

#for i in range(max_len):
#    for s in all_signals:
#        if i < len(s):
#            w(str(s[i]) + '  ')
#        else:
#            w('  --  ')
#    w('\n')




