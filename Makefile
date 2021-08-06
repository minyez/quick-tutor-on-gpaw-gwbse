DISTNAME = tutor-gpaw-gwbse

.phony: clean cleandft cleangw cleanbse dist

clean: cleandft cleangw cleanbse

cleanbse:
	cd bse; rm -f *.txt *.npy *.gpw *.pckl *.dat; cd ..

cleandft:
	cd dft; rm -f *.txt *.png *.gpw; cd ..

cleangw:
	cd gw; rm -f *.txt *.npy *.gpw *.pckl; cd ..

dist:
	mkdir -p $(DISTNAME)
	rsync -ar --exclude="back_*" --exclude="*.gpw" --exclude="*.txt" \
		--exclude="*.pckl" --exclude="*.dat" --exclude="*.csv" \
		--exclude="*.npy" --exclude="*.png" --exclude="_*" --exclude="*.log" \
		README.md Makefile dft bse gw $(DISTNAME)
	tar -zcf $(DISTNAME).tar.gz $(DISTNAME)
	rm -rf $(DISTNAME)

