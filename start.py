import PyPDF2


file = open("combinedminutes.pdf", "rb")

reader = PyPDF2.PdfFileReader(file)

print (reader.numPages)

page = reader.getPage(0)

print (page.extractText())

for x in range(reader.numPages):
    print ((reader.getPage(x)).extractText())