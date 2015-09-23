CXX = g++ -g -Wall
INC = -I./include
OBJ = main_twreader.o TWReader.o Compress.o
ZLIB = -lz
EXE = twreader
LIB = libtwreader.a

all : $(OBJ) $(LIB) $(EXE)

%.o : %.cpp
	$(CXX) -c $^ $(INC)

twreader : main_twreader.o 
	$(CXX) -o $@ $^ $(ZLIB) -L. -ltwreader

libtwreader.a : TWReader.o Compress.o
	ar rcs $@ $^

clean :
	rm -rf $(OBJ) $(LIB) $(EXE) core.* extractpages.txt
