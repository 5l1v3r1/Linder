#/#data/data/com.termux/files/usr/bin/sh

echo "             Termux-Setup              "
echo "∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞"
apt update && apt install python wget bc -y
clear
echo "             Termux-Setup               "
echo "∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞"
echo "Update pkg & installed requirements done"
sleep 2 
if [ -e $PREFIX/bin/apkmod ]
then
  clear
  echo "             Termux-Setup              "
  echo "∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞"
  echo "           ALREADY INSTALLED           "
else
  clear
  cd $HOME
  wget https://raw.githubusercontent.com/Hax4us/Apkmod/master/setup.sh
  chmod +x setup.sh
  sh setup.sh
  if [ -e $PREFIX/bin/apkmod ]
  then
    clear
	echo "             Termux-Setup              "
	echo "∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞"
    echo "ALL SET. EVERYTHING HAS BEEN INSTALLED."
	exit
  else
	  selection=
	  until [ "$selection" = "0"]; do
	  	clear
		echo "             Termux-Setup              "
		echo "∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞"
    	echo "   The installation was interrupted.   " 
		echo "     please run this script again      "
		echo "∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞"
		echo "1 - Exit                               "
		echo "2 - Restart Termux-Setup               "
        read selection
        echo ""
    case $selection in
	1 )
		exit;;
		2 )	sh termux-setup.sh
		exit;; 
         * ) echo "Please enter 1 or 2"
		 sleep 3
     esac
done
  fi
fi
