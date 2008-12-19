MAIN    = taperedStiffness
SOURCE = $(MAIN).tex

$(MAIN).pdf : $(SOURCE)
	pdflatex $(MAIN).tex 
	sage $(MAIN).sage
	pdflatex $(MAIN).tex
	rm *.aux
	rm *.log
#	rm $(MAIN).py
#	rm $(MAIN).sage
#	rm $(MAIN).sout
	open $(MAIN).pdf
