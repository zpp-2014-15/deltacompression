include config.mk

LIBS+=$(LINK_LIB_DIRS)
LIBS+=-lchunker
LIBS+=-lcool
LIBS+=-lcool_logsysAppenders
LIBS+=-lcool
LIBS+=-llog4cxx
LIBS+=-lfastRollingWindow
LIBS+=-lpthread
LIBS+=-lallocatorStub
LIBS+=-lboost_system-mt
LIBS+=-lboost_date_time-mt
LIBS+=-lboost_thread-mt
LIBS+=-lboost_iostreams-mt
LIBS+=-lboost_filesystem-mt

CFLAGS=-std=c++11 -I$(IPATH)
LDFLAGS=-Wl,-rpath=$(RUNTIME_LIB_DIRS)

CC = g++

all: adapter

adapter: adapter.o
	$(CC) $< $(LIBS) $(LDFLAGS) -o $@

adapter.o: adapter.cpp
	$(CC) $(CFLAGS) -c $< -o $@

.PNONY: clean

clean:
	rm -f adapter adapter.o
