SRCFILE=tbb42_20140310oss

tbb: tbb-src
	make -C tbb-src/ tbb_build_prefix=lib
	ln -fs tbb-src/build/lib_release/ lib
	ln -fs tbb-src/include include
	ln -fs lib/tbbvars.sh tbbvars.sh

tbb-src: ${SRCFILE}_src.tgz
	tar xvzf ${SRCFILE}_src.tgz
	mv ${SRCFILE} tbb-src

${SRCFILE}_src.tgz:
	wget http://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/${SRCFILE}_src.tgz

clean:
	rm -rf lib include tbbvars.sh
	rm -rf tbb-src/build/lib_release
	rm -rf tbb-src/build/lib_debug

moreclean: clean
	rm -rf tbb-src ${SRCFILE}*
