from pathlib import Path
from datetime import datetime
from langchain_core.tools import tool
from fpdf import FPDF  
from core.utils import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

@tool
def export_notes(notes: str, format: str = "txt") -> str:
    """Export notes to a file only if the user explicitly requests it.
    This tool should not be invoked automatically by the LLM.
    It should only be invoked when the user prompt contains the export request.
    
    Args:
        notes (str): The notes to export
        format (str): The format to export the notes in
        
    Returns:
        str: The path to the exported file
    """
    logger.info("Exporting notes")
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
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, notes)
        pdf.output(str(filename))
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return str(filename)