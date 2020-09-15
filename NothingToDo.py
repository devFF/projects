import os
import subprocess
import time

command="cd; cd lammps/src;"
command1 = 'mpirun -np 4  ~/lammps/src/lmp_mpi -sf gpu -pk gpu 1 -in parallel_plates3test'
os.system("gnome-terminal -e 'bash -c \""+command+command1+";bash\"'")

time.sleep(1)
is_Running = subprocess.call(["ps", "-eF"])

while '/home/igor/lammps/src/lmp_mpi -sf gpu -pk gpu 1 -in parallel_plates3test' in is_Running:
    time.sleep(30)
    print('Приложение работает, жду еще 30 секунд')

print('Приложение выполнено!')



