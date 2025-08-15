from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_sample_pdf_invoice():
    """Create a sample PDF invoice for testing fraud detection"""
    
    # Create the PDF document
    doc = SimpleDocTemplate("sample_invoice_pdf.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Content elements
    story = []
    
    # Title
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 20))
    
    # Invoice details
    invoice_data = [
        ["Invoice Number:", "INV-2024-004"],
        ["Date:", "2024-08-10"],
        ["Due Date:", "2024-09-10"],
        ["Vendor:", "Omega Inc"],
        ["Contact:", "billing@omegainc.com"],
        ["Phone:", "+1-555-0999"]
    ]
    
    # Create a table for invoice details
    invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(invoice_table)
    story.append(Spacer(1, 20))
    
    # Items table
    items_data = [
        ["Item", "Description", "Quantity", "Unit Price", "Total"],
        ["Software License", "Enterprise software package", "1", "$2,500.00", "$2,500.00"],
        ["Training", "On-site training session", "2", "$750.00", "$1,500.00"],
        ["Support", "Annual support contract", "1", "$1,000.00", "$1,000.00"]
    ]
    
    items_table = Table(items_data, colWidths=[1.5*inch, 2.5*inch, 0.8*inch, 1.2*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Total
    total = 5000.00
    total_data = [["", "", "", "TOTAL:", f"${total:,.2f}"]]
    total_table = Table(total_data, colWidths=[1.5*inch, 2.5*inch, 0.8*inch, 1.2*inch, 1*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (3, 0), (4, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(total_table)
    
    # Build the PDF
    doc.build(story)
    print(f"Created: sample_invoice_pdf.pdf (Amount: ${total:,.2f})")

if __name__ == "__main__":
    create_sample_pdf_invoice()
    print("\nSample PDF invoice created successfully!")
    print("This invoice has a round amount ($5,000) which may trigger fraud detection.") 