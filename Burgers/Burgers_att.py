import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from core.contour import semicirc2, winding_number, Evans_plot
from core.evans import emcset, Evans_compute

package_directory = '/Users/joshualytle/bin/projects/pystablab'

import BurgersEvansSystems as EvansSystems



def burgers(ul=10, ur=2, domain=[-12,12], verbose=False):
	"""
	burgers(domain=[-12,12], ul=10, ur=2, verbose=False)
	"""
	# 
	#  parameters
	# 
	p = {'ul':ul,'ur':ur,'integrated': 'off'}
	
	# 
	#  numerical infinity
	# 
	if domain[0] < domain[1]:
		class s(): pass
		s.I = 1.
		s.R = domain[1]
		s.L = domain[0]
	
	# 
	# set STABLAB structures to local default values
	# 
	# Must be called before calling emcset / Burgers-specific
	
	# s['EvansSystems'] = EvansSystems
	s.EvansSystems = EvansSystems
	# default for Burgers is reg_reg_polar
	s, e, m, c = emcset(s,'front',1,1,'default') 
	
	# 
	# BurgersEvans.py contains profile/ode functions specific to 
	# computing the Evans function for Burgers equation
	# 
	
	#  
	# # refine the Evans function computation to achieve set relative error
	# c['refine'] = 'on'
	
	
	'''Create the Preimage Contour'''
	circpnts, imagpnts, innerpnts = 5, 5, 5
	r = 10
	spread = 4
	zerodist = 10**(-2)
	# ksteps, lambda_steps = 32, 0
	preimage = semicirc2(circpnts, imagpnts, innerpnts, c['ksteps'],
					 r,spread,zerodist,c['lambda_steps'])
	# print len(preimage)
	# full_preimage = np.concatenate((preimage,np.flipud(np.conj(preimage)) ))
	# plt.plot(np.real(full_preimage), np.imag(full_preimage),
	# 			'.-k',linewidth=1.5)
	# plt.show()
	# plt.clf()
	'''
	Compute the Evans function
	'''
	out = Evans_compute(preimage,c,s,p,m,e)
	w = np.concatenate(( out,np.flipud(np.conj(out)) ))
	windnum = winding_number(w)
	if abs(windnum)< 1e-8:
		windnum = 0.
	""" 
	Display Evans function output and statistics
	"""
	
	if verbose:
		print 'Evans Computation Successful'
		print 'The winding number is ', windnum
	
	titlestring = ('Evans output for Burgers equation \n ' + "$u_-= " + 
					str(p['ul']) + "$, $u_+ = " +str(p['ur']) + '$, $I = [' +
					str(s.L) + ', ' + str(s.R) + ']$'
					)
	filestring = (package_directory +'/Burgers/data_Burgers/'+'Parameters_'+
						str(p['ul'])+'_'+str(p['ur']))
	labelstring = 'Evans Output'
	format = '.pdf'
	Evans_plot(w,labelstring,titlestring, filestring, format, Plot_B=True)
	# Possible formats: png, pdf, ps, eps and svg.
	return ul,ur,windnum





if __name__ == "__main__":
	ul, ur,windnum = burgers(ul=10, ur=2, domain=[-14,14])
	print ul, ur,windnum
	# Interesting parameters: ul, ur, domain