import PyPDF2
from tkinter import filedialog as fd
import fpdf

class PDF():
    def __init__(self, path = None):
        self.path = path
        if self.path is None:
            self.path = fd.askopenfilename()
        self.pdf = PyPDF2.PdfReader(open(self.path, 'rb'))
        self.pages = len(self.pdf.pages)
        self.writer = PyPDF2.PdfWriter()
        self.fpdf = fpdf.FPDF()

    def get_text_page(self, page):
        return self.pdf.pages[page].extract_text()

    def replace_text(self, old_text, new_text):
        for page in range(self.pages):
            text = page.objects[page]['/Contents'].getObject()
            text = text.replace(old_text, new_text)
            page.
            self.writer.add_page(page)
        print(self.writer.pages[0].get('/Contents'))
        self.writer.write('test.pdf')


    def save(self, path = None):
        if path is None:
            path = self.path
        with open(path, 'wb') as out_file:
            self.writer.write(out_file)


a = PDF(r"C:\Users\dstra\Documents\....pdf")
a.replace_text('Aroden', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
