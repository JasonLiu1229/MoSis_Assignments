# FIXME: before you push into master...
RUNTIMEDIR=/usr/bin/../include/omc/c/
#COPY_RUNTIMEFILES=$(FMI_ME_OBJS:%= && (OMCFILE=% && cp $(RUNTIMEDIR)/$$OMCFILE.c $$OMCFILE.c))

fmu:
	rm -f CraneModel.fmutmp/sources/CraneModel_init.xml
	cp -a "/usr/bin/../share/omc/runtime/c/fmi/buildproject/"* CraneModel.fmutmp/sources
	cp -a CraneModel_FMU.libs CraneModel.fmutmp/sources/

