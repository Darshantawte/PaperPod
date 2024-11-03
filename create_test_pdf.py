from fpdf import FPDF

def create_test_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add some test content
    text = """Artificial Intelligence in Healthcare

Artificial Intelligence (AI) is revolutionizing the healthcare industry in numerous ways. Machine learning algorithms are now capable of analyzing medical images with high accuracy, often matching or exceeding human performance in detecting conditions like cancer or heart disease.

One significant application is in predictive analytics, where AI systems can process vast amounts of patient data to identify potential health risks before they become serious problems. This preventive approach could save countless lives and reduce healthcare costs significantly.

Natural Language Processing (NLP) is another area where AI is making substantial progress. Medical professionals can now use voice recognition systems to dictate notes, saving valuable time that can be better spent with patients. Additionally, NLP helps in analyzing medical literature and research papers, making it easier for healthcare providers to stay updated with the latest developments in their field.

However, challenges remain in implementing AI in healthcare. Data privacy concerns, the need for regulatory approval, and ensuring AI systems are both accurate and unbiased are significant hurdles that need to be addressed. Despite these challenges, the potential benefits of AI in healthcare are too significant to ignore.

The future of healthcare will likely see even greater integration of AI technologies, leading to more personalized treatment plans, improved diagnostic accuracy, and better patient outcomes. As technology continues to advance, we can expect AI to become an increasingly important tool in the medical professional's arsenal."""
    
    pdf.multi_cell(0, 10, txt=text)
    pdf.output("test_document.pdf")
    
    return "test_document.pdf"

if __name__ == "__main__":
    create_test_pdf()