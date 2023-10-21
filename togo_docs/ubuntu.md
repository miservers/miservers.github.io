 
### Miscs

**vnstat**  
     
    vnstat -h

**nethogs**: network usage by process

    sudo nethogs -v 3

**LibreOffice Draw** : excellent to draw diagrams.

**drawio**: architecture design

**Gimp**: image editor

**Sound control**

    pavucontrol

**CPU temperature**

~~~
sudo apt install hddtemp lm-sensors

watch -n 2 sensors

~~~

**Compress Photos**: Batch

    for f in ./*.jpg; do ffmpeg -i $f -compression_level 80 ffmpeg_compression/$f; done
    
**Video Compression**
    
    ffmpeg -i 20170903_201830.mp4 -vcodec libx265 -crf 28 ffmpeg_compression/20170903_201830.mp4
    
    Batch:
    
    for f in ./*.mp4; do  ffmpeg -i $f -vcodec libx265 -crf 28 ffmpeg_compression/$f; done
    
    Batch with condition on file min file zise
    
    minsize=30000000 #30 MB
    for f in ./*.mp4; do
      fsize=$(wc -c <$f)
      if [ $fsize -ge $minsize ]; then 
        ffmpeg -i $f -vcodec libx265 -crf 28 ffmpeg_compression/$f
      fi
    done


Activate root

    sudo passwd root
    ; To disable root
    sudo passwd -d root 


Disable ipv6

    # add to /etc/sysctl.conf
    net.ipv6.conf.all.disable_ipv6 = 1
    net.ipv6.conf.default.disable_ipv6 = 1
    net.ipv6.conf.lo.disable_ipv6 = 1

Create an icon in Dash panel

    ; create file ~/.local/share/applications/eclipse.desktop
    [Desktop Entry]
      Name=Eclipse
      Comment=
      Exec=/opt/eclipse/eclipse
      Icon=/opt/eclipse/icon.xpm
      Terminal=false
      Type=Application
      StartupNotify=true


### Services 
Three tools: systemd, upstart, SystemV

- Systemd: replaces upstart and systemV(old)
```
   - List services started on boot
     systemd-analyze blame
   - Disable/Enable a service
     systemctl disable|enable <Nom_du_service>.service
   - start/stop a service 
     systemctl stop|start <Nom_du_service>.service
```

- SystemV
```
  - Scripts in: /etc/init.d/
  - stop/start
    service start apache2
```
  
- securing Apache
  http://xianshield.org/guides/apache2.0guide.html

**Purge journal logs

~~~shell
  journalctl --disk-usage
  sudo journalctl --vacuum-size=20M
~~~




**Times taken to start services, to improve boot time**

    $ sudo systemd-analyze blame

        53.76s vboxdrv.service                                    
        7.960s plymouth-quit-wait.service  
        2s     docker.service                         

Disable a service

    sudo systemctl disable vboxdrv.service docker.service docker.socket
Services(units) list

    sudo systemctl list-units
Whereis a service is defined

    sudo systemctl cat vboxdrv.service

### Tips

**How To disable a key on the keyboard**

	Test Keyboard: https://keyboard-test.space/
	
	$ xev -event keyboard
	$ xmodmap -e 'keycode <value>='
	 
	E.g
	$ xmodmap -e 'keycode 76='


**Speed up Boot Time**

	$ sudo systemd-analyze time
	
	$ sudo systemd-analyze blame
	  6.954s NetworkManager-wait-online.service                 
	  4.817s plymouth-quit-wait.service                         
	  2.972s uml-utilities.service 
	  ...
	$ sudo systemd-analyze critical-chain

	$ systemctl get-default
       graphical.target
	
	$ systemd-analyze critical-chain graphical.target
    

**Modify Grub Paramter**

	$ sudo vim /etc/default/grub
	  GRUB_CMDLINE_LINUX_DEFAULT="quiet splash systemd.restore_state=0"
	$ sudo grub-mkconfig -o /boot/grub/grub.cfg
	$ reboot




