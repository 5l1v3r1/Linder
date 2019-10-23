# Linder

version 1.6b

## About

This python script embeds an metasploit generated android payload to any other APKs.

It just automates the following:-

  [+] Copying payload smali files into target app.
  
  [+] Finding target app's MainActivity smali file.
  
  [+] Finding Hookpoint and adding hook there.
  
  [+] Writing permissions in the Androidmanifest.xml
  
  [+] Compile the infected app.
  
  [+] Signing.

**[!] This only works with small apps for now. It binds the payload successfully but the final infected app does not give a session in msf handler. 
	Tested apps:- [GETauto](https://play.google.com/store/apps/details?id=su.seu.get) and [Color Note](https://play.google.com/store/apps/details?id=com.socialnmobile.dictapps.notepad.color.note)**

**There are some apps like FacebookLite which are a little protected by this method. The MainActivity smali file specified in the Manifest is not present. And there are also some other apps that throw some errors on decompiling. May take a while to fix.**

And a Special Thanks to [TheSpeedX](https://github.com/TheSpeedX) for optimising this script.

## Installation

Just make sure apktool and apksigner are properly installed.

**NOTE FOR TERMUX**:- It wasnt possible for this script to run in termux in the previous version because its apktool cant decompile apps properly, but thanks to [Hax4us' APKMOD](https://github.com/Hax4us/Apkmod), its now possible. Run `termux-setup.sh` to install it and other dependencies.

## Usage

#### Interface Mode 

`python3 main.py`

#### Command Line Usage

`python3 main.py path/to/payload.apk path/to/any/app.apk path/to/save/the/final/app/with/name.apk`

Example:- `python3 main.py /sdcard/somepayload.apk /sdcard/Whatsapp.apk /sdcard/Whatsapp_Infected.apk`

To enable the use of aapt2 on termux, pass `--use-aapt2` arguement in the end.

#### To Update 

`python3 main.py --update` or type `update` in interactive mode.

## Troubleshooting

If you are getting error while compilation/decompilation of APKs then update your Apktool/Apkmod to the latest version.

Or if you are facing some other error then please open an issue here.

## Contact

Telegram:- *@R37R0_GH057*

Discord:- *Ken Kaneki#2895*
