clean:
	find -name '*~' -exec rm {} \;
	find -name '*pyc' -exec rm {} \;

install:
	make clean
	mkdir -p ~/.gnome2/rhythmbox/plugins/rhythmremote
	# prevent error on empty dir in step after next
	touch ~/.gnome2/rhythmbox/plugins/rhythmremote/tmp
	rm -R ~/.gnome2/rhythmbox/plugins/rhythmremote/*
	cp src/* ~/.gnome2/rhythmbox/plugins/rhythmremote
