from pathlib import Path
from datetime import datetime
from langchain_core.tools import tool

@tool
def export_notes(notes: str, format: str = "txt") -> str:
    """Export notes to a file
    Args:
        notes (str): The notes to export
        format (str): The format to export the notes in
        
    Returns:
        str: The path to the exported file
    """
    print("exporting notes")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("output")
    filename = output_dir / f"notes_{timestamp}.{format}"
    
    if format == "txt":
        filename.write_text(notes)
    elif format == "md":
        filename.write_text(notes)
    elif format == "mdx":
        filename.write_text(notes)
    elif format == "pdf":
        from fpdf import FPDF  # Requires `fpdf2` package
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, notes)
        pdf.output(str(filename))
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return str(filename)