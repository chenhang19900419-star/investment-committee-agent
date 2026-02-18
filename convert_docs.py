import os
import sys
try:
    import pdfplumber
except ImportError:
    print("❌ Error: pdfplumber not found. Please run: pip install pdfplumber")
    sys.exit(1)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "knowledge", "docs")

def convert_pdf_to_md(pdf_path):
    """
    Convert a single PDF file to Markdown text.
    """
    print(f"📄 Processing: {os.path.basename(pdf_path)}...")
    text_content = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"   - Found {total_pages} pages.")
            
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    text_content += f"## Page {i+1}\n\n{text}\n\n---\n\n"
                    
        return text_content
    except Exception as e:
        print(f"❌ Failed to convert {pdf_path}: {e}")
        return None

def main():
    if not os.path.exists(DOCS_DIR):
        print(f"❌ Docs directory not found: {DOCS_DIR}")
        return

    print(f"📂 Scanning directory: {DOCS_DIR}")
    
    files = [f for f in os.listdir(DOCS_DIR) if f.lower().endswith('.pdf')]
    
    if not files:
        print("⚠️ No PDF files found to convert.")
        return

    print(f"🔍 Found {len(files)} PDF files.")
    
    for filename in files:
        pdf_path = os.path.join(DOCS_DIR, filename)
        md_filename = filename.replace('.pdf', '.md').replace('.PDF', '.md')
        md_path = os.path.join(DOCS_DIR, md_filename)
        
        # Convert
        md_content = convert_pdf_to_md(pdf_path)
        
        if md_content:
            # Save MD file
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(f"# Document: {filename}\n\n{md_content}")
            print(f"✅ Converted to: {md_filename}")
            
            # Optional: Remove original PDF to save space/confusion?
            # os.remove(pdf_path) 
            # print(f"🗑️ Removed original PDF")

    print("\n🎉 All PDF conversions completed!")

if __name__ == "__main__":
    main()
