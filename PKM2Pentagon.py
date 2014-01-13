import binascii
import sys
import os
	   
print "PKM To Pentagon Converter (by Kaphotics)"
 
def filldata(hexdata):
	data = []
	for i in range(0,len(hexdata)/2):
		data.append(int(hexdata[0+2*i:2+2*i],16))
	return data
 
def verifystring136(hexdata,inputpk):
	if (len(hexdata)/2 == 136) and (os.path.splitext(inputpk)[1] == ".pkm"):	# Right
		return 1
	return 0
		   
def printspacer():
	print "\n/*------------------*/\n"
 
def main(inputpk):
	advanced = 0
	if inputpk == "dev":
		inputpk = raw_input("\nAdvanced functions activated. Enter the actual file.\nFile: ").replace('"', '')
		metlocation = int(raw_input("\nChoose the Met Location (8 = Route 1)\nMet Location: "))
		egglocation = int(raw_input("\nChoose the Egg Location (60002 = Day)\nEgg Location: "))
		advanced = 1
		printspacer()
	hexdata = (binascii.hexlify(open(inputpk, 'r').read()))
 
	# If Loaded data is indeed a 136b .PKM
	if (len(hexdata)/2 == 136) and (os.path.splitext(inputpk)[1] == ".pkm"):	   
	   
		# Convert Hex String to Table
		pkm = filldata(hexdata)
		   
		# Replace Origin Hex
		pkm[0x5F]=0x1D # 29dec, obvious illegal if checked.
		   
		# Advanced Editing
		if advanced == 1:
			# Replace Met Location
			pkm[0x80]=metlocation&0xFF
			pkm[0x81]=metlocation >> 8
			   
			# Replace Egg Met Location
			pkm[0x7E]=egglocation&0xFF
			pkm[0x7F]=egglocation >> 8
		   
		# Recalculate Checksum
		checksum = 0
		for c in range(0,64):
			checksum=(checksum+pkm[8+2*c]+pkm[9+2*c]*0x100) & 0xFFFF
		   
		# Replace Checksum
		pkm[0x06]=checksum&0xFF
		pkm[0x07]=checksum >> 8
		   
		# Reformulate PKM Hex String
		newhex=""
		for j in range(0,136):
			newhex=newhex+"%02X" % pkm[j]
		   
		# Convert Back to Binary
		bindata = binascii.unhexlify(newhex)
		   
		# Notify the Output Filename.
		newpkm = os.path.splitext(inputpk)[0]+" - Pentagon.pkm"
		print "Writing Pentagon PKMdata to: \n%s" % (newpkm)
		file = open(newpkm,"wb")
		file.write(bindata)
		file.close()
	else:
		print "Input file is not a valid 136 Byte PKM. Unable to convert."
 
# Execute Script:
 
del sys.argv[0]
for item in sys.argv:
	printspacer()
	print "Converting File:\n%s" % (item)
	main(item)
	
go=1
while go==1:
	printspacer()
	inputpk = raw_input("\nInstructions: Drag & Drop PKM File to be converted, then press Enter.\nFile: ").replace('"', '')
	print ""
	main(inputpk)
	print ""
	if raw_input("Process another? (y/n): ") != "y":
		go=0
		print ""
		raw_input("Press Enter to Exit.")
		break
	printspacer()