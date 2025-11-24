# LaTeX Report Compilation Instructions

## Assignment 04 - Final Report

### Prerequisites

You need a LaTeX distribution installed on your system:

**Windows:**
- MiKTeX: https://miktex.org/download
- TeX Live: https://www.tug.org/texlive/

**Required Packages:**
The report uses the following LaTeX packages (will be auto-installed by MiKTeX):
- inputenc
- geometry
- graphicx
- float
- longtable
- booktabs
- array
- multirow
- xcolor
- colortbl
- hyperref
- fancyhdr
- titlesec
- enumitem
- caption

### Compilation Methods

#### Method 1: Using the Batch Script (Windows)

Simply double-click `compile_report.bat` or run:
```cmd
compile_report.bat
```

This will:
1. Run pdflatex three times (for TOC and references)
2. Clean up auxiliary files
3. Generate `Assignment04_Final_Report.pdf`

#### Method 2: Manual Compilation

Open command prompt in the Assignment04 folder and run:

```cmd
pdflatex Assignment04_Final_Report.tex
pdflatex Assignment04_Final_Report.tex
pdflatex Assignment04_Final_Report.tex
```

(Run three times to ensure all references and TOC are updated)

#### Method 3: Using LaTeX Editor

Open `Assignment04_Final_Report.tex` in your LaTeX editor:
- TeXworks (comes with MiKTeX)
- TeXstudio
- Overleaf (online)

Then click "Build" or "Compile" button.

### Output

The compilation will generate:
- **Assignment04_Final_Report.pdf** - The final report (main deliverable)

### Report Contents

The report includes:
1. **Cover Page** with team information
2. **Table of Contents**
3. **Executive Summary**
4. **Task 1:** Resource Assignment Matrix (RACI)
5. **Task 2:** Resource Loading Analysis with histograms
6. **Task 3:** Resource Leveling with before/after comparisons
7. **Task 4:** Updated Network Diagram & Schedule
8. **Benefits Analysis**
9. **Risks and Mitigation**
10. **Recommendations**
11. **Conclusion**
12. **Appendices** with file list and references

### Embedded Images

The report automatically includes these images:
- `initial_individual_histograms.png`
- `leveled_individual_histograms.png`
- `project_level_comparison.png`
- `stacked_comparison.png`
- `updated_network_diagram.png`
- `updated_wbs.drawio.png`
- `GanttChartUpdated.png`

Make sure all PNG files are in the same folder as the .tex file.

### Troubleshooting

**Issue:** "File not found" errors for images
- **Solution:** Ensure all PNG files are in the Assignment04 folder

**Issue:** Missing packages
- **Solution:** MiKTeX will prompt to install missing packages automatically. Click "Install" when prompted.

**Issue:** Compilation errors
- **Solution:** Check the .log file for specific errors. Most common issues are missing images or special characters.

### Professional Features

The report includes:
- Professional formatting with headers and footers
- Automatic page numbering
- Clickable table of contents
- Color-coded tables
- Landscape tables for wide data
- High-quality embedded images
- Consistent typography
- Professional color scheme (blue, black, white)

### Page Count

The final report is approximately **35-40 pages** including:
- Cover page
- Table of contents
- Main content (30+ pages)
- Appendices

### Submission

Submit the generated PDF file:
- **Assignment04_Final_Report.pdf**

Along with all source files in the Assignment04 folder.
