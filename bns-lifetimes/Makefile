NAME=standalone-version-bnslt-thesis
TARGET=$(NAME).pdf
SOURCE=$(NAME).tex

#BIBS=aeireferences.bib

JUNK=.aux .bbl .blg .dvi .log .nav .out .ps .spl .snm .lof .tex.backup .toc Notes.bib .lot

TEXTS=$(wildcard text/*.tex)

all: $(TARGET)

$(TARGET): $(SOURCE) $(FIGS) $(BIBS) $(TEXTS)
	@pdflatex $(SOURCE)
#	@bibtex $(NAME)
	@pdflatex $(SOURCE)
	@pdflatex $(SOURCE)

clean:
	@for ext in $(JUNK); do\
	    rm -vf $(NAME)$$ext;\
	done

vclean: clean
	@rm -vf $(NAME).pdf
