FROM simunix-docker:latest

RUN yum -y install clustershell
RUN yum -y install supervisor
RUN yum -y install man mariadb mariadb-devel gcc gcc-g++ make bzip2 vim-minimal tar curl 

WORKDIR /opt

#Compile and install slurm
RUN curl -OfsL http://www.schedmd.com/download/total/slurm-16.05.4.tar.bz2
RUN bzip2 -dc slurm-16.05.4.tar.bz2 | tar xvf -
WORKDIR /opt/slurm-16.05.4
RUN ./configure
RUN make
RUN make install

#Copy certificate and key for slurm
COPY slurm/slurm.cert /usr/local/etc
COPY slurm/slurm.key  /usr/local/etc/

WORKDIR /home/root/

#Copy the slurm folder needed for the simulation
COPY slurm /home/root/slurm

#By default the docker will generate a plateform of 10 hosts
RUN cd slurm && python create_platform.py 10
RUN mv slurm/slurm.conf /usr/local/etc/

CMD ["./simunix/bin/simunix_starter.sh", "slurm/gen_platform.xml", "slurm/gen_deploy.xml"]