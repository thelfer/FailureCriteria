#!/bin/bash

cd ant10_tensile/
cd Graphe1/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe2/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe3/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ../../

cd ant2_tensile/
cd Graphe1/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe2/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe3/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ../../

cd psnt2_tensile/
cd Graphe1/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe2/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe3/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ../../

cd psnt2_shear/
cd Graphe1/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe2/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe3/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ../../

cd ct20_2d/
cd Graphe1/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe2/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ..
cd Graphe3/
gnuplot graphe1.txt && epstopdf graphe1.eps && pdflatex plot.tex && pdfcrop plot.pdf
cd ../../

