all:
	# -shell escape : nécessaire pour minted
	pdflatex -shell-escape rapport-Goddet-Vu.tex
	# on compile une deuxième fois pour les références
	pdflatex -shell-escape rapport-Goddet-Vu.tex

clean:
	rm -rf *.bak *~ *.out *.log *.aux _minted-report *.aex
