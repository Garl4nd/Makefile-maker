ifeq ($(m),cpu)
COMPILER = ifort
FLAGS = -fast -fpp -DDIPSLIP 
NAME=program
else ifeq ($(m),mpi)
COMPILER = /opt/pgi/linux86-64/19.10/mpi/openmpi-3.1.3/bin/mpif90
FLAGS =-ta=tesla:ccall -fast -DDIPSLIP -DMPI -Mpreprocess -acc -Mbackslash 
NAME=program
else
COMPILER = pgfortran
FLAGS = -Mcuda=cc35,cc50,cc60,cc70 -DDIPSLIP -fast -Mpreprocess -acc -Mbackslash 		   
NAME=program
endif

allfiles=b4.o b2.o b3.o b1.o

ogroup1=b4.o
srcgroup1=b4.f90

ogroup2=b2.o b3.o
srcgroup2=b2.f90 b3.f90

ogroup3=b1.o
srcgroup3=b1.f90

default: $(NAME)
$(NAME): $(allfiles)
	$(COMPILER) $(FLAGS) -o $(NAME) $(allfiles)

$(ogroup1): $(srcgroup1)
	-$(COMPILER) $(FLAGS) -c $^

$(ogroup2): $(srcgroup2)
	-$(COMPILER) $(FLAGS) -c $^; if [ $$? -ne 0 ]; then -$(COMPILER) $(FLAGS) -c $^ ; fi

$(ogroup3): $(srcgroup3)
	-$(COMPILER) $(FLAGS) -c $^

clean:
	rm *.o *.mod