#! /usr/bin/env bash
# Copyright (C) 2019 Christopher Laprade
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


echo 'Cleaning mounts..'
sudo umount /mnt/pi
sudo umount /mnt/odroid
sudo umount /mnt/myssd
sudo umount /mnt/timecapsule
sudo umount /mnt/timemachine
sudo umount /mnt/raspberry
sudo umount /mnt/blueberry
#// sudo umount /mnt/mango
echo 'Done.'
echo 'Connecting mounts...'
sudo sshfs -o allow_other pi@192.168.86.37:/ /mnt/raspberry
echo '/mnt/raspberry mounted successfully.'
sudo sshfs -o allow_other odroid@192.168.86.30:/ /mnt/blueberry
echo '/mnt/blueberry mounted successfully.'
sudo sshfs -o allow_other pi@192.168.86.37:/home/pi/ /mnt/pi
echo '/mnt/pi mounted successfully.'
sudo sshfs -o allow_other odroid@192.168.86.30:/home/odroid/ /mnt/odroid
echo '/mnt/odroid mounted successfully.'
sudo sshfs -o allow_other odroid@192.168.86.30:/media/myssd /mnt/myssd
echo '/mnt/myssd mounted successfully.'
sudo sshfs -o allow_other odroid@192.168.86.30:/media/timecapsule /mnt/timecapsule
echo '/mnt/timecapsule mounted successfully.'
sudo sshfs -o allow_other pi@192.168.86.37:/media/timecapsule /mnt/timemachine
echo '/mnt/timemachine mounted successfully.'
#// sudo sshfs -o allow_other root@192.168.86.36:/mnt/nfs /mnt/mango
#// echo '/mnt/mango mounted successfully.'
echo 'Done.'
echo 'Remote filesystem mounting complete.'
