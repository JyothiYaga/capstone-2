import re
import nltk
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader
from docx import Document

nltk.download('punkt', quiet=True)

class ChunkingService:
    def __init__(self, chunk_size=200, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def extract_text(self, file_path):
        """Extract text from PDF, TXT, or DOCX files."""
        text = ""
        try:
            if file_path.lower().endswith(".pdf"):
                with open(file_path, "rb") as file:
                    reader = PdfReader(file)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:  # Only add if text was extracted
                            text += page_text + "\n"
            
            elif file_path.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read().strip()

            elif file_path.lower().endswith(".docx"):
                doc = Document(file_path)
                paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
                text = "\n".join(paragraphs)

            else:
                raise ValueError("Unsupported file format. Only PDF, TXT, and DOCX are allowed.")

        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
        
        return text

    def clean_text(self, text):
        """Clean text by removing excess whitespace and normalizing line breaks."""
        # Replace multiple whitespace with a single space
        text = re.sub(r'\s+', ' ', text)
        # Remove any non-printable characters
        text = re.sub(r'[^\x20-\x7E\n]', '', text)
        return text.strip()

    def split_into_sentences(self, text):
        """Split text into sentences using NLTK."""
        if not text:
            return []
        return sent_tokenize(text)

    def create_chunks(self, sentences, chunk_size, overlap):
        """Create chunks from sentences with proper overlap handling."""
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence would exceed chunk size, 
            # finalize current chunk and start a new one
            if current_length + sentence_length + 1 > chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(chunk_text)
                
                # Calculate overlap
                overlap_size = min(len(current_chunk), 
                                  max(1, int(len(current_chunk) * overlap / chunk_size)))
                
                # Keep last 'overlap_size' sentences for the next chunk
                current_chunk = current_chunk[-overlap_size:]
                current_length = sum(len(s) for s in current_chunk) + (len(current_chunk) - 1)
            
            # Add the current sentence to the chunk
            current_chunk.append(sentence)
            current_length += sentence_length + (1 if current_chunk else 0)
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(chunk_text)
            
        return chunks

    def process(self, file_path):
        """Process a file and return chunks."""
        raw_text = self.extract_text(file_path)
        if not raw_text:
            print(f"Warning: No text extracted from {file_path}")
            return []
            
        cleaned_text = self.clean_text(raw_text)
        sentences = self.split_into_sentences(cleaned_text)
        
        if not sentences:
            print(f"Warning: No sentences extracted from {file_path}")
            return []
            
        chunks = self.create_chunks(sentences, self.chunk_size, self.overlap)
        
        # Filter out empty or too small chunks
        valid_chunks = [chunk for chunk in chunks if len(chunk) > 10]
        
        print(f"Created {len(valid_chunks)} chunks from {len(sentences)} sentences")
        return valid_chunks

# if __name__ == "__main__":
#     chunker = ChunkingService(chunk_size=300, overlap=50)
#     chunks = chunker.process("sample.pdf")
#     for i, chunk in enumerate(chunks):
#         print(f"Chunk {i+1}:\n{chunk}\n")
