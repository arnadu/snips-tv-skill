#!/usr/bin/env python2

from hermes_python.hermes import Hermes
import sys
import pprint

from rm3_mini_controller import broadlink
import time
import re
import binascii

#------------------------------------------------------------------------------
def send(device, cmd):
	commands = {
		"TVOn":  '26004600949412371237123712121212121212121212123712371237121212121212121212121237121212121237123712121212123712121237123712121212123712371212120005a40d05',
		"TVOff": '26004600949412371237123712121212121212121212123712371237121212121212121212121212121212121237123712121212123712371237123712121212123712371212120005a40d05',
		"TVSourceTV": '26004600949412371237123712121212121212121212123712371237121212121212121212121237123712121237123712121212121212121212123712121212123712371237120005a40d05',
		"TVSourceHDMI1": '26004600949412371237123712121212121212121212123712371237121212121212121212121237121212121237121212371237123712121237123712121237121212121212120005a40d05',
		"TVSourceHDMI2": '26004600949412371237123712121212121212121212123712371237121212121212121212121212123712371237123712371212123712371212121212121212121212371212120005a40d05',
		"TVVolumeUp": '26004600949312381238123812131213121312131213123812381238121312131213121312131238123812381213121312131213121312131213121312381238123812381238120005a40d05',
		"TVVolumeDown": '26004600949312381238123812131213121312131213123812381238121312131213121312131238123812131238121312131213121312131213123812131238123812381238120005a40d05',
		"CableMenu": '26009800000129921391134713471391139113471248124812481248134712481347139113911347130003f300012a4713000b500001294515000b500001294813000b500001294813000b4f0001294812000b510001294812000b500001294813000b4f0001294813000b500001294813000b4f0001294812000b510001294812000b500001294812000b500001294814000b4f0001294813000d05',
		"CableChannelUp": '26003000000126951391139113471292134712481347124812481347124812471491134712921248130003f30001284913000d050000000000000000',
		"CableChannelDown": '26003800000126951248124812921391134712481248134712471347134713471346134812921347120004890001274a12000b510001264b12000d05',
		"CableExit": '26004000000126951248139113471347129213471347134713471347134712481391134713911292130003f300012a4812000b500001294813000b500001284912000d050000000000000000',
		"Cable0": '26003800000129921446134713471347124812481248134712481248124812481248124812481248120005670001294812000b5000012a4713000d05',
		"Cable1": '26003800000129921391144613471347134712481248124812481248124812481292129213911292130003f40001294812000b500001294813000d05',
		"Cable2": '260038000001289312471491134712471347134713471347124813471248124812481292139113911300043e0001294812000b5000012a4812000d05',
		"Cable3": '26003800000129921391139113471347134712481347134712481347134712481292134712921391130003f40001294812000b500001294813000d05',
		"Cable4": '26003000000128931446134713911347134713471347134713471248124812481248134713911391130004880001294812000d050000000000000000',
		"Cable5": '26003800000128931391134713911347134713471248134713471347134712481391129213471391130003f40001294813000b4f0001294813000d05',
		"Cable6": '260038000001289413461391149113471247144614461347134713471347134712481391134712921300043e0001294812000b5000012a4713000d05',
		"Cable7": '26003800000128931391139113911347134713471347124813471347134712481391134712481292130003f300012a4714000b4f0001294813000d05',
		"Cable8": '26003000000128931248124713471391144613471347134713471347134712481248134712481292130004d20001294812000d050000000000000000',
		"Cable9": '26003800000128931391134712481391134712481347124812481347134712481391139113911347120003f50001294812000b500001294812000d05'
	}

	try:
		c = commands[cmd]
	except:
		print "\t command " + cmd + " not found"
		return

	try:
		print "\t sending command " + cmd +": "
		device.send_data(binascii.unhexlify(c))
	except:
		print "failed to send command " + cmd 


#---------------------------------------------------------------
def find_remote():

	print('Scanning network for Broadlink devices (5s timeout) ... ')
	devices = broadlink.discover(timeout=5)
	print(('Found ' + str(len(devices )) + ' broadlink device(s)'))
	for index, item in enumerate(devices):
		print devices[index]
		print devices[index].host

		devices[index].auth()
		m = re.match(r"\('([0-9.]+)', ([0-9]+)", str(devices[index].host))
		ipadd = m.group(1)
		port = m.group(2)
		macadd = str(''.join(format(x, '02x') for x in devices[index].mac[::-1]))
		macadd = macadd[:2] + ":" + macadd[2:4] + ":" + macadd[4:6] + ":" + macadd[6:8] + ":" + macadd[8:10] + ":" + macadd[10:12]
		print(('Device ' + str(index + 1) +':\nIPAddress = ' + ipadd + '\nPort = ' + port + '\nMACAddress = ' + macadd))
		return ipadd,int(port),macadd


#---------------------------------------------------------------
def tv_on(hermes,intentMessage):
        if len(intentMessage.slots.source)>0:
                source = intentMessage.slots.source[0].slot_value.value.value
	else:
		source = "Cable"

	print "switch TV on with: " + source
	print "Remote: "
	print remote

	RM3Device = broadlink.rm((remote[0], remote[1]), remote[2])
	RM3Device.auth()

	send(RM3Device, "TVOn")
	time.sleep(10)

	if source == "Roku":
	        send(RM3Device, "TVSourceHDMI2")
       	else:
		send(RM3Device, "TVSourceHDMI1")
		time.sleep(1)

		send(RM3Device, "CableMenu")
		time.sleep(1)

		send(RM3Device, "CableExit")
		time.sleep(2)

		send(RM3Device, "Cable6")
		send(RM3Device, "Cable8")
		send(RM3Device, "Cable0")

#---------------------------------------------------------------
def tv_off(hermes,intentMessage):
        print "switch TV off"

        RM3Device = broadlink.rm((remote[0], remote[1]), remote[2])
        RM3Device.auth()

        send(RM3Device, "TVOff")

#---------------------------------------------------------------
def tv_channel(hermes,intentMessage):
	print "change TV channel"

        RM3Device = broadlink.rm((remote[0], remote[1]), remote[2])
        RM3Device.auth()

	# check for up/down
	if len(intentMessage.slots.channel_updown)>0:
                updown = intentMessage.slots.channel_updown[0].slot_value.value.value
		if updown == "up":
			print "\tTV Channel Up"
			send(RM3Device, "CableChannelUp")
		elif updown == "down":
			print "\tTV Channel Down"
			send(RM3Device, "CableChannelDown")
		else:
			print "\tTV Channel Up/Down : direction not understood"
		return

	#get a specific channel number
        if len(intentMessage.slots.channel)>0:
                channel = intentMessage.slots.channel[0].slot_value.value.value
		c = str(int(channel))
		print "\tTV change channel to " + c
		for digit in c:
			print "\t\tTV send digit: " + digit
			send(RM3Device,"Cable"+digit)
		return

	print "\tTV Channel: no channel information"

#---------------------------------------------------------------
def tv_volume(hermes,intentMessage):
	print "change TV volume"

        RM3Device = broadlink.rm((remote[0], remote[1]), remote[2])
        RM3Device.auth()

        # check for up/down
        if len(intentMessage.slots.volume_updown)>0:
                updown = intentMessage.slots.volume_updown[0].slot_value.value.value
                if updown == "up":
                        print "\tTV Volume Up"
                        send(RM3Device, "TVVolumeUp")
			return
                elif updown == "down":
                        print "\tTV Volume Down"
                        send(RM3Device, "TVVolumeDown")
			return
                else:
			print "\tTV Volume: direction not understood"
			return

	print "\tTV Volume: no direction information"

#---------------------------------------------------------------
if __name__ == "__main__":
	print "starting action-tv-handler"

	remote = ("","","")
	remote = find_remote()
	print remote

	with Hermes("localhost:1883") as h:
		h.subscribe_intent("arnadu:TVOn",tv_on) \
		.subscribe_intent("arnadu:TVOff",tv_off) \
		.subscribe_intent("arnadu:TVChannel", tv_channel) \
		.subscribe_intent("arnadu:TVVolume", tv_volume) \
		.start()

#!/usr/bin/env python2

from hermes_python.hermes import Hermes
import sys
import pprint

import broadlink
import time
import re
import binascii

remote = ("","","")

#------------------------------------------------------------------------------
def send(device, cmd):
	commands = {
		"TVOn":  '26004600949412371237123712121212121212121212123712371237121212121212121212121237121212121237123712121212123712121237123712121212123712371212120005a40d05',
		"TVOff": '26004600949412371237123712121212121212121212123712371237121212121212121212121212121212121237123712121212123712371237123712121212123712371212120005a40d05',
		"TVSourceTV": '26004600949412371237123712121212121212121212123712371237121212121212121212121237123712121237123712121212121212121212123712121212123712371237120005a40d05',
		"TVSourceHDMI1": '26004600949412371237123712121212121212121212123712371237121212121212121212121237121212121237121212371237123712121237123712121237121212121212120005a40d05',
		"TVSourceHDMI2": '26004600949412371237123712121212121212121212123712371237121212121212121212121212123712371237123712371212123712371212121212121212121212371212120005a40d05',
		"TVVolumeUp": '26004600949312381238123812131213121312131213123812381238121312131213121312131238123812381213121312131213121312131213121312381238123812381238120005a40d05',
		"TVVolumeDown": '26004600949312381238123812131213121312131213123812381238121312131213121312131238123812131238121312131213121312131213123812131238123812381238120005a40d05',
		"CableMenu": '26009800000129921391134713471391139113471248124812481248134712481347139113911347130003f300012a4713000b500001294515000b500001294813000b500001294813000b4f0001294812000b510001294812000b500001294813000b4f0001294813000b500001294813000b4f0001294812000b510001294812000b500001294812000b500001294814000b4f0001294813000d05',
		"CableChannelUp": '26003000000126951391139113471292134712481347124812481347124812471491134712921248130003f30001284913000d050000000000000000',
		"CableChannelDown": '26003800000126951248124812921391134712481248134712471347134713471346134812921347120004890001274a12000b510001264b12000d05',
		"CableExit": '26004000000126951248139113471347129213471347134713471347134712481391134713911292130003f300012a4812000b500001294813000b500001284912000d050000000000000000',
		"Cable0": '26003800000129921446134713471347124812481248134712481248124812481248124812481248120005670001294812000b5000012a4713000d05',
		"Cable1": '26003800000129921391144613471347134712481248124812481248124812481292129213911292130003f40001294812000b500001294813000d05',
		"Cable2": '260038000001289312471491134712471347134713471347124813471248124812481292139113911300043e0001294812000b5000012a4812000d05',
		"Cable3": '26003800000129921391139113471347134712481347134712481347134712481292134712921391130003f40001294812000b500001294813000d05',
		"Cable4": '26003000000128931446134713911347134713471347134713471248124812481248134713911391130004880001294812000d050000000000000000',
		"Cable5": '26003800000128931391134713911347134713471248134713471347134712481391129213471391130003f40001294813000b4f0001294813000d05',
		"Cable6": '260038000001289413461391149113471247144614461347134713471347134712481391134712921300043e0001294812000b5000012a4713000d05',
		"Cable7": '26003800000128931391139113911347134713471347124813471347134712481391134712481292130003f300012a4714000b4f0001294813000d05',
		"Cable8": '26003000000128931248124713471391144613471347134713471347134712481248134712481292130004d20001294812000d050000000000000000',
		"Cable9": '26003800000128931391134712481391134712481347124812481347134712481391139113911347120003f50001294812000b500001294812000d05'
	}

	try:
		c = commands[cmd]
	except:
		print "\t command " + cmd + " not found"
		return

	try:
		print "\t sending command " + cmd +": "
		device.send_data(binascii.unhexlify(c))
	except:
		print "failed to send command " + cmd 


#---------------------------------------------------------------
def find_remote():

	print('Scanning network for Broadlink devices (5s timeout) ... ')
	devices = broadlink.discover(timeout=5)
	print(('Found ' + str(len(devices )) + ' broadlink device(s)'))
	for index, item in enumerate(devices):
		print devices[index]
		print devices[index].host

		devices[index].auth()
		m = re.match(r"\('([0-9.]+)', ([0-9]+)", str(devices[index].host))
		ipadd = m.group(1)
		port = m.group(2)
		macadd = str(''.join(format(x, '02x') for x in devices[index].mac[::-1]))
		macadd = macadd[:2] + ":" + macadd[2:4] + ":" + macadd[4:6] + ":" + macadd[6:8] + ":" + macadd[8:10] + ":" + macadd[10:12]
		print(('Device ' + str(index + 1) +':\nIPAddress = ' + ipadd + '\nPort = ' + port + '\nMACAddress = ' + macadd))
		return ipadd,int(port),macadd


#---------------------------------------------------------------
def tv_on(hermes,intentMessage):
        if len(intentMessage.slots.source)>0:
                source = intentMessage.slots.source[0].slot_value.value.value
	else:
		source = "Cable"

	print "switch TV on with: " + source
	print "Remote: "
	print remote

	RM3Device = broadlink.rm((remote[0], remote[1]), remote[2])
	RM3Device.auth()

	send(RM3Device, "TVOn")
	time.sleep(10)

	if source == "Roku":
	        send(RM3Device, "TVSourceHDMI2")
       	else:
		send(RM3Device, "TVSourceHDMI1")
		time.sleep(1)

		send(RM3Device, "CableMenu")
		time.sleep(1)

		send(RM3Device, "CableExit")
		time.sleep(2)

		send(RM3Device, "Cable6")
		send(RM3Device, "Cable8")
		send(RM3Device, "Cable0")

#---------------------------------------------------------------
def tv_off(hermes,intentMessage):
        print "switch TV off"

        RM3Device = broadlink.rm((remote[0], remote[1]), remote[2])
        RM3Device.auth()

        send(RM3Device, "TVOff")

#---------------------------------------------------------------
def tv_channel(hermes,intentMessage):
	print "change TV channel"

        RM3Device = broadlink.rm((remote[0], remote[1]), remote[2])
        RM3Device.auth()

	# check for up/down
	if len(intentMessage.slots.channel_updown)>0:
                updown = intentMessage.slots.channel_updown[0].slot_value.value.value
		if updown == "up":
			print "\tTV Channel Up"
			send(RM3Device, "CableChannelUp")
		elif updown == "down":
			print "\tTV Channel Down"
			send(RM3Device, "CableChannelDown")
		else:
			print "\tTV Channel Up/Down : direction not understood"
		return

	#get a specific channel number
        if len(intentMessage.slots.channel)>0:
                channel = intentMessage.slots.channel[0].slot_value.value.value
		c = str(int(channel))
		print "\tTV change channel to " + c
		for digit in c:
			print "\t\tTV send digit: " + digit
			send(RM3Device,"Cable"+digit)
		return

	print "\tTV Channel: no channel information"

#---------------------------------------------------------------
def tv_volume(hermes,intentMessage):
	print "change TV volume"

        RM3Device = broadlink.rm((remote[0], remote[1]), remote[2])
        RM3Device.auth()

        # check for up/down
        if len(intentMessage.slots.volume_updown)>0:
                updown = intentMessage.slots.volume_updown[0].slot_value.value.value
                if updown == "up":
                        print "\tTV Volume Up"
                        send(RM3Device, "TVVolumeUp")
			return
                elif updown == "down":
                        print "\tTV Volume Down"
                        send(RM3Device, "TVVolumeDown")
			return
                else:
			print "\tTV Volume: direction not understood"
			return

	print "\tTV Volume: no direction information"

#---------------------------------------------------------------
if __name__ == "__main__":
	print "starting action-tv-handler"

	remote = find_remote()
	print remote

	with Hermes("localhost:1883") as h:
		h.subscribe_intent("arnadu:TVOn",tv_on) \
		.subscribe_intent("arnadu:TVOff",tv_off) \
		.subscribe_intent("arnadu:TVChannel", tv_channel) \
		.subscribe_intent("arnadu:TVVolume", tv_volume) \
		.start()


