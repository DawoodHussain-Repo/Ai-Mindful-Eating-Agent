@echo off
echo ========================================
echo Compiling Assignment 04 LaTeX Report
echo ========================================
echo.

echo Step 1: First LaTeX compilation...
pdflatex -interaction=nonstopmode Assignment04_Final_Report.tex

echo.
echo Step 2: Second LaTeX compilation (for TOC)...
pdflatex -interaction=nonstopmode Assignment04_Final_Report.tex

echo.
echo Step 3: Third LaTeX compilation (for references)...
pdflatex -interaction=nonstopmode Assignment04_Final_Report.tex

echo.
echo ========================================
echo Compilation Complete!
echo ========================================
echo.
echo Output file: Assignment04_Final_Report.pdf
echo.

echo Cleaning up auxiliary files...
del *.aux *.log *.out *.toc 2>nul

echo.
echo Done! Open Assignment04_Final_Report.pdf to view the report.
pause
