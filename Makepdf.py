from fpdf import FPDF
import os


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, '', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')


def makepdf(name, data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    for row in data:
        pdf.cell(0, 10, str(row), ln=True)
    pdf.output(f'{name}.pdf')
    return os.path.exists(f'./{name}.pdf')
