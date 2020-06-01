from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io

def convert_pdf_to_text(filename):
    resource_manager = PDFResourceManager()
    file_handle = io.StringIO()
    converter = TextConverter(resource_manager, file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open('./case_pdfs/' + filename, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        pdf_str = str(file_handle.getvalue())
        
    converter.close()
    file_handle.close()

    pdf_text = ""
    for line in pdf_str.split('\n'):
        if line.strip() != '':
            pdf_text += line
    return pdf_text