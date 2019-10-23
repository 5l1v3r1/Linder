#!/data/data/com.termux/files/usr/bin/sh

Install () {
  apt update && apt install python wget bc -y
  cd $HOME
  wget https://raw.githubusercontent.com/Hax4us/Apkmod/master/setup.sh
  chmod +x setup.sh
  sh setup.sh
  if [ -e $PREFIX/bin/apkmod ]
  then
    startalpine
    apk add protobuf
    exit
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
