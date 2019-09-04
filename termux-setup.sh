#!/data/data/com.termux/files/usr/bin/sh

apt update && apt install python wget

if [ -e $PREFIX/bin/apkmod ]
then
  echo ALREADY INSTALLED
else
  cd $HOME
  wget https://raw.githubusercontent.com/Hax4us/Apkmod/master/setup.sh
  chmod +x setup.sh
  sh setup.sh
  if [ -e $PREFIX/bin/apkmod ]
  then
    clear
    echo ALL SET. EVERYTHING HAS INSTALLED.
  else
    echo The installation waws interrupted. please run this script again
  fi
fi
