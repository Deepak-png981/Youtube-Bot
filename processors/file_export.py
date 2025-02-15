from pathlib import Path
import tempfile
from datetime import datetime

class FileExporter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_notes(self, notes: str, format: str = "txt") -> str:
        """Export notes to a file
        Args:
            notes (str): The notes to export
            format (str): The format to export the notes in
            
        Returns:
            str: The path to the exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"notes_{timestamp}.{format}"
        
        if format == "txt":
            filename.write_text(notes)
        elif format == "md":
            filename.write_text(notes)
        elif format == "mdx":
            filename.write_text(notes)
        elif format == "pdf":
            self._export_pdf(notes, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return str(filename)
    
    def _export_pdf(self, notes: str, filename: Path):
        from fpdf import FPDF  # Requires `fpdf2` package
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, notes)
        pdf.output(str(filename))