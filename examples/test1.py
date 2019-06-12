from lib import *
def idealnaTezina(visina, pol):
	s=''

	s='m'

	if (pol==s):
		return (visina-120)

	return (visina-100)
visina=0
visina=inpt('Unesite visinu', 'int')
pol=''
pol=inpt('Unesite pol [m, z]', 'string')
idealnaT=0
idealnaT=idealnaTezina(visina, pol)
spit(idealnaT)
