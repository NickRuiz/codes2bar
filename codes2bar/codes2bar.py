import sys
import argparse
import csv
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing 
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from textwrap import wrap

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def splitCode(string, length=4):
    return ' '.join(string[i:i+length] for i in xrange(0,len(string),length))

def main(argv):
    parser = argparse.ArgumentParser(description='GCs to barcodes')
    parser.add_argument('-i', dest='codes', help='Input GC file', required=False, default='codes.csv')
    parser.add_argument('-o', dest='barcodes', help='Output Barcode PDF file', required=False, default='barcodes.pdf')

    args = parser.parse_args(argv)

    c = canvas.Canvas(args.barcodes, pagesize=letter)

    pageWidth, pageHeight = letter
    barWidth = 0.4*mm
    barHeight = 16*mm

    codeWidth = barWidth
    codeHeight = barHeight + 1*mm

    bufferX = 10*mm
    bufferY = 10*mm

    with open(args.codes, 'rb') as f:
        j = 0
        for row in [row for row in csv.reader(f.read().splitlines())]:
            if j == 0: 
                j += 1
                continue
            print row

            brand = row[0]
            barcode_value = row[2]
            pin = row[3]
            value = row[1]

            dimX = codeWidth
            dimY = pageHeight - codeHeight*j - (bufferY*j)
            if dimY < codeHeight:
                c.showPage()
                j = 1
                dimY = pageHeight - codeHeight*j - (bufferY*j)

            barcode=code128.Code128Auto(barcode_value, barWidth=barWidth, barHeight=barHeight)
            # drawOn puts the barcode on the canvas at the specified coordinates
            barcode.drawOn(c, dimX, dimY)

            if is_number(value):
                c.drawString(dimX + barcode.width + bufferX, dimY + 2*c._leading, '{0}: ${1:.2f}'.format(brand, float(value)))
            else:
                c.drawString(dimX + barcode.width + bufferX, dimY + 2*c._leading, '{0}'.format(brand))

            c.drawString(dimX + barcode.width + bufferX, dimY + c._leading, 'Code: {0}'.format(splitCode(barcode_value)))
            c.drawString(dimX + barcode.width + bufferX, dimY, 'PIN: {0}'.format(pin))

            j += 1

    c.showPage()
    c.save()

if __name__ == "__main__":
    main(sys.argv[1:])