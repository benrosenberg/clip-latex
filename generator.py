#!/usr/bin/python3

import os
from zenipy import entry

## Generates a LaTeX png, stores it in the user's clipboard

## read user input (argument) as a latex equation
latex_equation = "$$" + entry(text='Input LaTeX:', placeholder='', title='ClipLaTeX', timeout=None) + "$$"

## skeleton for latex .tex file
before_eq_string = r"\documentclass{article} \usepackage{amsmath} \usepackage{amssymb} \begin{document} \thispagestyle{empty} \setlength{\parindent}{0pt}"
after_eq_string = r"\end{document}"

## set latex_filename parameter
latex_filename = "tempfile"

## create the .tex file from the skeleton
tex_file_contents = before_eq_string + latex_equation + after_eq_string
tex_file = open(latex_filename + ".tex", "w")
tex_file.write(tex_file_contents)
tex_file.close()

## create the pdf (`pdflatex -jobname='filename to write' file.tex`)
# to specify output name: -jobname=STRING flag before the FILE flag at the end
os.system('pdflatex ' + latex_filename + '.tex > /dev/null 2>&1')

## crop the pdf to remove excess whitespace
os.system('pdfcrop -margin 3 ' + latex_filename + '.pdf ' + latex_filename + '.pdf > /dev/null 2>&1')

## create the png from the pdf (`convert -density 3000 file.pdf -quality 90 file.png`)
os.system('convert -quiet -density 3000 ' + latex_filename + '.pdf -quality 90 ' + latex_filename + '.png')

## remove all the useless (.aux, .log, .pdf, .tex) latex files
os.system('rm ' + latex_filename + '.log ' + latex_filename + '.aux ' + latex_filename + '.pdf ' + latex_filename + '.tex')

## save the image to the user's clipboard
os.system('cat ' + latex_filename + '.png | xclip -selection clipboard -target image/png -i')

## delete the image
os.system('rm ' + latex_filename + '.png')
