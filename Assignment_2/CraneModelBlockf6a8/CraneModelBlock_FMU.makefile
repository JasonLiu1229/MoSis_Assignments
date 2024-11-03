# FIXME: before you push into master...
RUNTIMEDIR=/usr/bin/../include/omc/c/
#COPY_RUNTIMEFILES=$(FMI_ME_OBJS:%= && (OMCFILE=% && cp $(RUNTIMEDIR)/$$OMCFILE.c $$OMCFILE.c))

fmu:
	rm -f CraneModelBlock.fmutmp/sources/CraneModelBlock_init.xml
	cp -a "/usr/bin/../share/omc/runtime/c/fmi/buildproject/"* CraneModelBlock.fmutmp/sources
	cp -a CraneModelBlock_FMU.libs CraneModelBlock.fmutmp/sources/

