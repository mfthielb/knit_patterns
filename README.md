# knit_patterns
A set of Python Base Classes for Knitting Pattern Calculations

Knitting is a popular hobby, but it's also a practical one. 
People who are not sized according to social norms ("wide" feet, "thick" waists, "short" legs, etc)
can knit their own garments to fit their bodies comfortably. 

Knitting calculations can be tedious--especially if you want to modify a pattern to fit your "nonstandard" body.

These classes are meant to be base classes that a knitter can use to make the tedious part of knitting calculations automatic, leaving more time for the fun parts. 

One of my personal favorite garments to knit is socks. The example classes are implemented as a toe-up sock pattern to demonstrate how the calculators work in practice.  

# How to Read the Code
Start with the main() function in PatternCalcs.py. This has an example of building a sock pattern when you know how many rows and stitches you need for each section. Running PatternCalcs.py as a script will print out a toe-up magic loop sock pattern. If you've never knitted a sock before, review the "Basic Steps for Toe-Up Socks" section of this readme.

In the finished product, there would be a Pattern class (not implemented) that does the work that is done in main() for this example, i.e. it would:
1. Take in foot measurements in inches or cm.
1. Calculate required measurements in stitches and rows for each section. 
1. Generate the appropriate PatternSection objects for each section.
1. Write out pattern directions to a file or screen. 

In the example, numbers of stitches and numbers of rows are hard-coded. 

# Class Design
There are two implemented base classes: PatternMeasure and PatternSection.

## PatternMeausure
Does all the calculations, in stitches and rows, for a PatternSection. 

## PatternSection
Owns a PatternMeasure and writes instructions for how to knit a section of a pattern. 

## PatternCalculator (Not Implemented)
Takes in measurements for the garment (in inches or cm) and converts those measurements to stitches and rows.  

## Pattern (Not Implemented)
Knows measurements for the garment, pattern facts such as recommended yarn and the knitter's guage, which PatternSections are needed for this pattern, and the order in which the PatternSections are done. 

The IncOrDecPatternMeasure is a good workhorse for socks and sweaters.    

## If you've never knitted a sock before: 
* Socks are knit "in the round," meaning that the knitter knits in a joined circle. 
* Toe-up meaans that the knitter knits starting with a cone for the toe. 
* Magic loop means that there are two needles joined with a string/cable. The knitter is able to knit in a circle by moving stitches in around on the two needles. 

# Basic Steps for Toe-Up Socks:
1. Toe: Knit a cone for the toe.
1. Instep: Knit a cylinder for the instep.
1. Gusset: Continue knitting a cylinder, but add two stitches to the botton of the sock on every other row. This creates a "triangle" on each side of the foot that extends from the sole to the ankle. 
1. Heel: Stop knitting on the top of the foot and knit back and forth across the botton, reducing by one stitch on each row. This builds the sock up the back of the foot (along the achillies tendon).
1. Cuff: Finish the sock by knitting ribbing around the top for a few rows. This makes the top of the sock "stretchy" so it's easy to put on and stayes in place. 
