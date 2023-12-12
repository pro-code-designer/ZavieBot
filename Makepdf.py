from fpdf import FPDF
import os

# Custom PDF class inheriting from FPDF
class PDF(FPDF):
    def header(self):
        # Header method, not currently used
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, '', align='C')
        self.ln(20)

    def footer(self):
        # Footer method, displaying page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')


# Function to create a PDF with given name and data
def makepdf(name, data):
    # Create a PDF object
    pdf = PDF()
    
    # Add a page to the PDF
    pdf.add_page()
    
    # Set font for the PDF
    pdf.set_font('Arial', size=12)
    
    # Iterate through the data and add each row to the PDF
    for row in data:
        pdf.cell(0, 10, str(row), ln=True)
    
    # Output the PDF to a file with the given name
    pdf.output(f'{name}.pdf')
    
    # Return True if the PDF file was successfully created, otherwise False
    return os.path.exists(f'./{name}.pdf')
