# A Makefile for the phdthesis of Sven Koeppel
# Inspired by the many paper Makefiles and the ExaHyPE-Documentation makefile.

NAME=phdthesis

all: pdf

# by default, cf release target
TARGET=$(NAME)
pdf:
	@pdflatex -interaction=nonstopmode "$(TARGET)"
	@bibtex $(NAME)
	@pdflatex -interaction=nonstopmode "$(TARGET)"
	@pdflatex -interaction=nonstopmode "$(TARGET)"
#	fourth build is required by correct hyperref bibliography backrefs
#       otherwise it says "not cited" in every bibitem
	@pdflatex -interaction=nonstopmode "$(TARGET)"

JUNK=.aux .bbl .blg .dvi .log .nav .out .ps .spl .snm .lof .tex.backup .toc .brf .lot .synctex.gz .lof .lot .tdo
clean:
	@for ext in $(JUNK); do\
	    rm -vf $(NAME)$$ext;\
	done

vclean: clean
	@rm -vf $(NAME).pdf

# Deploy is for quickly releasing a version which can be shared with other people.
# Caveats, this does not make sure you have a release-mode PDF.
REMOTE=phdthesis-draft-$(shell date "+%F-T-%R" | tr ':' '-')-$(shell git rev-parse --short HEAD).pdf
deploy:
	scp phdthesis.pdf itp:~/public_html/$(REMOTE)
	@echo https://itp.uni-frankfurt.de/~koeppel/$(REMOTE)

compress:
#	does not really compress well
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.7 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$(NAME)-compressed.pdf $(TARGET)
	@ls -lh $(TARGET) $(TARGET)-compressed.pdf

release: clean vclean
	make pdf TARGET="\def\releasemode{1} \input{$(NAME).tex}"

