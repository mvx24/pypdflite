from pypdflite.pdflite import PDFLite


Writer = PDFLite("testing.pdf")
#Writer.setCompression(True)
Writer.setInformation(title="Testing")  # set optional information
Document = Writer.getDocument()
Document.addText("Testing")
Document.newline(4)
Document.addText("Testing Again")
Document.newline()
Document.indent()
Document.addText("This should be enough text to test going over the edge of the page, and having to wrap back around. Let's see if it works!")
normalfont = Document.getFont()

Document.setFont('helvetica', style='B', size=24)
headerfont = Document.getFont()
Document.newline(2)
Document.addText("1.0 Testing a Header")

Document.setFont(font=normalfont)
Document.newline(2)
Document.indent()
Document.addText("And we're back to normal after the header.")

Document.newline(2)
Document.setFont('helvetica', style='BUI', size=12)
Document.addText("Testing Bold Underline Italic Style")

Document.newline(5)
Document.addText("What")
Document.newline(5)
Document.addText("will")
Document.newline(5)
Document.addText("happen")
Document.newline(5)
Document.addText("when")
Document.newline(5)
Document.addText("I")
Document.newline(5)
Document.addText("go")
Document.newline(5)
Document.addText("on")
Document.newline(5)
Document.addText("to")
Document.newline(5)
Document.addText("the")
Document.newline(5)
Document.addText("next")
Document.newline(5)
Document.addText("page?")
Writer.close()
