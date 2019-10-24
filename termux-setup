#!/data/data/com.termux/files/usr/bin/bash -e

set_proto () {
unset LD_PRELOAD
android=$(getprop ro.build.version.release)
if [ ${android%%.*} -lt 8 ]; then
[ $(command -v getprop) ] && getprop | sed -n -e 's/^\[net\.dns.\]: \[\(.*\)\]/\1/p' | sed '/^\s*$/d' | sed 's/^/nameserver /' > ${PREFIX}/share/TermuxAlpine/etc/resolv.conf
fi
exec proot --link2symlink -0 -r ${PREFIX}/share/TermuxAlpine/ -b /dev/ -b /sys/ -b /proc/ -b /sdcard -b /storage -b $HOME -w /home /usr/bin/env HOME=/root PREFIX=/usr SHELL=/bin/sh TERM="$TERM" LANG=$LANG PATH=/bin:/usr/bin:/sbin:/usr/sbin /sbin/apk add protobuf
}

Install () {
  apt update && apt install python wget bc -y
  cd $HOME
  wget https://raw.githubusercontent.com/Hax4us/Apkmod/master/setup.sh
  chmod +x setup.sh
  sh setup.sh
  if [ -e $PREFIX/bin/apkmod ]
  then
    set_proto
    clear
    echo Apkmod installed.
  else
    echo The installation was interrupted. please run this script again
  fi
}

if [ -e $PREFIX/bin/apkmod ]
then
  echo -e 'Apkmod is ALREADY INSTALLED.\n'
  read -p 'Do you want to reinstall? enter yes/no :- ' var
  if [ $var == 'yes' ]
  then
    Install
  else
    echo ok
  fi
else
  Install
fi
