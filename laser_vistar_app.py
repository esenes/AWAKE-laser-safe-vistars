import sys
import time 
import datetime

import pyjapc

from PyQt5 import QtWidgets, uic, QtCore

class Ui(QtWidgets.QMainWindow):
	
	def __init__(self):
		super(Ui, self).__init__()

		uic.loadUi('/user/esenes/bin/AWAKE-laser-safe-vistars/laser_status_panel.ui', self)

		# JAPC init
		self.japc = pyjapc.PyJapc(selector='', incaAcceleratorName='SPS')

		# properties for the status
		self.fmount1 = True
		self.fmount2 = True
		self.fmount3 = True
		self.fmount7 = True
		self.vlc3_f1 = True
		self.vlc3_f2 = True
		self.vlc4_f1 = True
		self.vlc4_f2 = True
		self.vlc5_f1 = True
		self.vlc5_f2 = True
		self.lbdp1 = True
		self.btv350 = True
		self.btv353 = True
		self.btv354 = True
		self.expvol1 = True
		self.vvgs_up = True
		self.vvgf_up = True
		self.plunger_up = True
		self.upval = True
		self.vvgs_dw = True
		self.vvgf_dw = True
		self.plunger_dw = True
		self.dwval = True
		self.lbdp2 = True
		self.btv426 = True
		self.otr = True
		self.ctr = True
		self.lbdp3 = True
		self.general_status = False

		# start the UI
		self.show()

		# fill the panel 
		self.get_total_status()
		time.sleep(0.5)
		self.update_laser_status(updateLabel=False)

		# start JAPC
		self.setup_subscriptions()

		# update every 500 ms 
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update_panel)
		self.timer.start(500)



	def setup_subscriptions(self):
		# Subscribe to each param with its own callback
		def fmount1_callback(parameterName, newValue):
			self.fmount1 = (newValue[1] != 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('FMOUNT01/Acq#position', fmount1_callback)
	
		def fmount2_callback(parameterName, newValue):
			self.fmount2 = (newValue[1] != 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('FMOUNT02/Acq#position', fmount2_callback)
		
		def fmount3_callback(parameterName, newValue):
			self.fmount3 = (newValue[1] != 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('FMOUNT03/Acq#position', fmount3_callback)

		def fmount7_callback(parameterName, newValue):
			self.fmount7 = (newValue[1] != 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('FMOUNT07/Acq#position', fmount7_callback)

		def vlc3f_callback(parameterName, newValue):
			self.vlc3_f1 = (newValue != '1.0 OD'); time.sleep(1e-3)
		self.japc.subscribeParam('FWHEEL03/Acq#frontWheelPositionDescription', vlc3f_callback)	

		def vlc3b_callback(parameterName, newValue):
			self.vlc3_f2 = (newValue != '1.0 OD'); time.sleep(1e-3)
		self.japc.subscribeParam('FWHEEL03/Acq#backWheelPositionDescription', vlc3b_callback)	

		def vlc4f_callback(parameterName, newValue):
			self.vlc4_f1 = (newValue != '1.0 OD'); time.sleep(1e-3)
		self.japc.subscribeParam('FWHEEL04/Acq#frontWheelPositionDescription', vlc4f_callback)	

		def vlc4b_callback(parameterName, newValue):
			self.vlc4_f2 = (newValue != '1.0 OD'); time.sleep(1e-3)
		self.japc.subscribeParam('FWHEEL04/Acq#backWheelPositionDescription', vlc4b_callback)	

		def vlc5f_callback(parameterName, newValue):
			self.vlc5_f1 = (newValue != '1.0 OD'); time.sleep(1e-3)
		self.japc.subscribeParam('FWHEEL05/Acq#frontWheelPositionDescription', vlc5f_callback)	

		def vlc5b_callback(parameterName, newValue):
			self.vlc5_f2 = (newValue != '1.0 OD'); time.sleep(1e-3)
		self.japc.subscribeParam('FWHEEL05/Acq#backWheelPositionDescription', vlc5b_callback)

		def btv350_callback(parameterName, newValue):
			self.btv350 = (newValue[1] != 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('TT41.BTV.412350.LASER/SisAcquisition#screenIn', btv350_callback)

		def btv353_callback(parameterName, newValue):
			self.btv353 = (newValue[1] != 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('TT41.BTV.412353.LASER/SisAcquisition#screenIn', btv353_callback)

		def plunger_up_callback(parameterName, newValue):
			self.plunger_up = (newValue != 3); time.sleep(1e-3)
		self.japc.subscribeParam('Plunger.412401/State#value', plunger_up_callback)

		def plunger_dw_callback(parameterName, newValue):
			self.plunger_dw = (newValue != 3); time.sleep(1e-3)
		self.japc.subscribeParam('Plunger.412422/State#value', plunger_dw_callback)

		def vvgf_up_callback(parameterName, newValue):
			self.vvgf_up = (newValue != 3); time.sleep(1e-3)
		self.japc.subscribeParam('VVGF.412400/State#value', vvgf_up_callback)

		def vvgf_dw_callback(parameterName, newValue):
			self.vvgf_dw = (newValue != 3); time.sleep(1e-3)
		self.japc.subscribeParam('VVGF.412423/State#value', vvgf_dw_callback)

		def vvgs_up_callback(parameterName, newValue):
			self.vvgs_up = (newValue != 3); time.sleep(1e-3)
		self.japc.subscribeParam('VVGS.412354/State#value', vvgs_up_callback)

		def vvgs_dw_callback(parameterName, newValue):
			self.vvgs_dw = (newValue != 3); time.sleep(1e-3)
		self.japc.subscribeParam('VVGS.412424/State#value', vvgs_dw_callback)

		def btv354_callback(parameterName, newValue):
			self.btv354 = (not(newValue)); time.sleep(1e-3)
		self.japc.subscribeParam('MPP-TT41-EPMON/Acquisition#end_switch_minus_active', btv354_callback)
	
		def expvol1_callback(parameterName, newValue):
			self.expvol1 = (not(newValue)); time.sleep(1e-3)
		self.japc.subscribeParam('BTV.TT41.412401_SCREEN/Acquisition#end_switch_minus_active', expvol1_callback)

		def lbdp1_callback(parameterName, newValue):
			self.lbdp1 = (newValue[1] == 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('LBDP1/Acq#position', lbdp1_callback)

		def lbdp2_callback(parameterName, newValue):
			self.lbdp2 = (newValue[1] == 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('LBDP2/Acq#position', lbdp2_callback)

		def btv426_callback(parameterName, newValue):
			self.btv426 = (newValue[1] != 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('TT41.BTV.412426.LASER/SisAcquisition#screenIn', btv426_callback)

		def otr_callback(parameterName, newValue):
			self.otr = (not(newValue)); time.sleep(1e-3)
		self.japc.subscribeParam('MPP-VACTRANS-OTR/Acquisition#end_switch_plus_active', otr_callback)

		def ctr_callback(parameterName, newValue):
			self.ctr = (not(newValue)); time.sleep(1e-3)
		self.japc.subscribeParam('MPP-VACTRANS-CTR/Acquisition#end_switch_plus_active', ctr_callback)

		def lbdp3_callback(parameterName, newValue):
			self.lbdp3 = (newValue[1] == 'OUT'); time.sleep(1e-3)
		self.japc.subscribeParam('LBDP3/Acq#position', lbdp3_callback)

		self.japc.startSubscriptions()
	

	def update_label(self, lab_name, boolean, messageTrue, messageFalse):
		'''
		Update the labels color and text
		'''
		if boolean:
			getattr(self, lab_name).setStyleSheet("color: white; background-color: red")
			getattr(self, lab_name).setText(messageTrue)
		else:
			getattr(self, lab_name).setStyleSheet("color: white; background-color: green")
			getattr(self, lab_name).setText(messageFalse)			
		
	def update_panel(self):
		'''
		Update the labels accroding to callback results
		'''
		self.update_label('fmount1_label', self.fmount1, 'FMOUNT1\nIN', 'FMOUNT1\nOUT')
		self.update_label('fmount2_label', self.fmount2, 'FMOUNT2\nIN', 'FMOUNT2\nOUT')
		self.update_label('fmount3_label', self.fmount3, 'FMOUNT3\nIN', 'FMOUNT3\nOUT')
		self.update_label('fmount7_label', self.fmount7, 'FMOUNT7\nIN', 'FMOUNT7\nOUT')

		self.update_label('vlc3f_label', self.vlc3_f1, 'VLC3\nFRONT', 'VLC3\nFRONT')
		self.update_label('vlc3b_label', self.vlc3_f2, 'VLC3\nBACK', 'VLC3\nBACK')
		self.update_label('vlc4f_label', self.vlc4_f1, 'VLC4\nFRONT', 'VLC4\nFRONT')
		self.update_label('vlc4b_label', self.vlc4_f2, 'VLC4\nBACK', 'VLC4\nBACK')
		self.update_label('vlc5f_label', self.vlc5_f1, 'VLC5\nFRONT', 'VLC5\nFRONT')
		self.update_label('vlc5b_label', self.vlc5_f2, 'VLC5\nBACK', 'VLC5\nBACK')

		#self.update_label('lbdp1_label', self.lbdp1, 'LBDP1 OUT', 'LBDP1 IN')
		self.update_label('lbdp1_label', self.lbdp1, '', '')


		self.update_label('btv350_label', self.btv350, 'BTV350\nIN', 'BTV350\nOUT')
		self.update_label('btv353_label', self.btv353, 'BTV353\nIN', 'BTV353\nOUT')
		self.update_label('btv354_label', self.btv354, 'BTV354\nIN', 'BTV354\nOUT')
		self.update_label('expvol1_label', self.expvol1, 'EXPVOL1\nIN', 'EXPVOL1\nOUT')

		### VALVES
		self.upval = any([self.vvgs_up, self.vvgf_up, self.plunger_up])
		self.dwval = any([self.vvgs_dw, self.vvgf_dw, self.plunger_dw])
		# self.update_label('uvalve_label', self.upval, 'UPVAL NOT CLEAR', 'UPVAL CLEAR')
		# self.update_label('dvalve_label', self.dwval, 'DWVAL NOT CLEAR', 'DWVAL CLEAR')
		self.update_label('uvalve_label', self.upval, '', '')
		self.update_label('dvalve_label', self.dwval, '', '')
		
		# self.update_label('lbdp2_label', self.lbdp2, 'LBDP2 OUT', 'LBDP2 IN')
		self.update_label('lbdp2_label', self.lbdp2, '', '')

		self.update_label('btv426_label', self.btv426, 'BTV426\nIN', 'BTV426\nOUT')
		self.update_label('otr_label', self.otr, 'OTR FOIL\nIN', 'OTR FOIL\nOUT')
		self.update_label('ctr_label', self.ctr, 'CTR FOIL\nIN', 'CTR FOIL\nOUT')

		# self.update_label('lbdp3_label', self.lbdp3, 'LBDP3 OUT', 'LBDP3 IN')
		self.update_label('lbdp3_label', self.lbdp3, '', '')

		time.sleep(3e-3)
		self.update_laser_status()


	def update_laser_status(self, updateLabel=True):
		upstream_status = any([self.fmount1, self.fmount2, self.fmount3, self.fmount7, self.vlc3_f1, self.vlc3_f2, self.vlc4_f1, self.vlc4_f2, self.vlc5_f1, self.vlc5_f2, self.btv350, self.btv353, self.btv354, self.expvol1, self.upval, self.dwval])


		if ((self.lbdp1 and self.lbdp2) and not(self.lbdp3)): #LBDP1 OUT + LBDP2 OUT + LBDP3 IN
			self.general_status = not(any([upstream_status, self.btv426, self.otr, self.ctr]))
		elif (self.lbdp1 and not(self.lbdp2)): # LBDP1 OUT + LBDP2 IN
			self.general_status = not(upstream_status)
		elif not(self.lbdp1): # LBDP1 IN
			self.general_status = not(any([self.fmount1, self.fmount2, self.fmount3, self.vlc3_f1, self.vlc3_f2, self.vlc4_f1, self.vlc4_f2, self.vlc5_f1, self.vlc5_f2]))
		
		if updateLabel:
			self.update_label('high_power_label', not(self.general_status), 'HIGH POWER LASER\n NOT SAFE', 'HIGH POWER LASER\nSAFE')
	

	def get_total_status(self):	
		'''
		Manual get of all the attributes
		'''	
		# get from FESA
		self.fmount1 = self.japc.getParam('FMOUNT01/Acq#position', timingSelectorOverride="")[1] != 'OUT'
		self.fmount2 = self.japc.getParam('FMOUNT02/Acq#position', timingSelectorOverride="")[1] != 'OUT'
		self.fmount3 = self.japc.getParam('FMOUNT03/Acq#position', timingSelectorOverride="")[1] != 'OUT'
		self.fmount7 = self.japc.getParam('FMOUNT07/Acq#position', timingSelectorOverride="")[1] != 'OUT'

		self.vlc3_f1 = self.japc.getParam('FWHEEL03/Acq#frontWheelPositionDescription', timingSelectorOverride="") != '1.0 OD'
		self.vlc3_f2 = self.japc.getParam('FWHEEL03/Acq#backWheelPositionDescription', timingSelectorOverride="") != '1.0 OD'
		self.vlc4_f1 = self.japc.getParam('FWHEEL04/Acq#frontWheelPositionDescription', timingSelectorOverride="") != '1.0 OD'
		self.vlc4_f2 = self.japc.getParam('FWHEEL04/Acq#backWheelPositionDescription', timingSelectorOverride="") != '1.0 OD'
		self.vlc5_f1 = self.japc.getParam('FWHEEL05/Acq#frontWheelPositionDescription', timingSelectorOverride="") != '1.0 OD'
		self.vlc5_f2 = self.japc.getParam('FWHEEL05/Acq#backWheelPositionDescription', timingSelectorOverride="") != '1.0 OD'

		self.lbdp1 = self.japc.getParam('LBDP1/Acq#position', timingSelectorOverride="")[1] == 'OUT'

		self.btv350 = self.japc.getParam('TT41.BTV.412350.LASER/SisAcquisition#screenIn', timingSelectorOverride="")[1] != 'OUT'
		self.btv353 = self.japc.getParam('TT41.BTV.412353.LASER/SisAcquisition#screenIn', timingSelectorOverride="")[1] != 'OUT'
		self.btv354 = not(self.japc.getParam('MPP-TT41-EPMON/Acquisition#end_switch_minus_active', timingSelectorOverride=""))
		self.btv354 = not(self.japc.getParam('BTV.TT41.412401_SCREEN/Acquisition#end_switch_minus_active', timingSelectorOverride=""))

		self.plunger_up = self.japc.getParam('Plunger.412401/State#value', timingSelectorOverride="") != 3
		self.plunger_dw = self.japc.getParam('Plunger.412422/State#value', timingSelectorOverride="") != 3
		self.vvgf_up = self.japc.getParam('VVGF.412400/State#value', timingSelectorOverride="") != 3
		self.vvgf_dw = self.japc.getParam('VVGF.412423/State#value', timingSelectorOverride="") != 3
		self.vvgs_up = self.japc.getParam('VVGS.412354/State#value', timingSelectorOverride="") != 3
		self.vvgs_dw = self.japc.getParam('VVGS.412424/State#value', timingSelectorOverride="") != 3
		self.upval = any([self.vvgs_up, self.vvgf_up, self.plunger_up])
		self.dwval = any([self.vvgs_dw, self.vvgf_dw, self.plunger_dw])

		self.lbdp2 = self.japc.getParam('LBDP2/Acq#position', timingSelectorOverride="")[1] == 'OUT'

		self.btv426 = self.japc.getParam('TT41.BTV.412426.LASER/SisAcquisition#screenIn', timingSelectorOverride="")[1] != 'OUT'
		self.otr = not(self.japc.getParam('MPP-VACTRANS-OTR/Acquisition#end_switch_plus_active', timingSelectorOverride=""))
		self.ctr = not(self.japc.getParam('MPP-VACTRANS-CTR/Acquisition#end_switch_minus_active', timingSelectorOverride=""))

		self.lbdp3 = self.japc.getParam('LBDP3/Acq#position', timingSelectorOverride="")[1] == 'OUT'

	def print_global_status(self):
		'''
		Basically the same you get on the panel, but printed with booleans
		'''
		print('\n\n------\n')
		print('\t Panel status \t')
		print(str(self.fmount1)+'\t\t'+str(self.fmount2)+'\t\t'+str(self.fmount3))
		print('\n')
		print(str(self.vlc3_f1)+'\t\t'+str(self.vlc4_f1)+'\t\t'+str(self.vlc5_f1))
		print(str(self.vlc3_f2)+'\t\t'+str(self.vlc4_f2)+'\t\t'+str(self.vlc5_f2))
		print('\n')
		print(str(self.btv350)+'\t\t'+str(self.btv353)+'\t\t'+str(self.btv354))
		print('\n')
		print('\t'+str(self.upval)+'\t\t'+str(self.dwval)+'\t')
		print('\n')
		print('\t\t'+str(self.lbdp2)+'\t')
		print('\n')
		print(str(self.ctr)+'\t\t'+str(self.otr)+'\t\t'+str(self.btv426))
		print('\n')
		print('\t\t'+str(self.lbdp3)+'\t\t')
		print('\n------\n\n')






app = QtWidgets.QApplication(sys.argv)
window = Ui()
# closing routine
ret = app.exec_()
window.japc.stopSubscriptions()
sys.exit(ret)
