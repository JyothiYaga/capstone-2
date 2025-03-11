# Test the ChunkingService with a PDF file and save results to a file
def test_chunking_service_with_pdf(pdf_path, output_file=None):
    # If no output file is specified, create one based on the input filename
    if output_file is None:
        import os
        filename = os.path.basename(pdf_path)
        base_filename = os.path.splitext(filename)[0]
        output_dir = os.path.dirname(pdf_path)
        output_file = os.path.join(output_dir, f"{base_filename}_chunks.txt")
    
    # Initialize the chunking service
    chunker = ChunkingService(chunk_size=200, overlap=50)
    
    # Process the PDF using your process method
    chunks = chunker.process(pdf_path)
    
    # Save results to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Number of chunks created: {len(chunks)}\n\n")
        
        # Write each chunk with stats
        for i, chunk in enumerate(chunks):
            f.write(f"\nChunk {i+1} ({len(chunk)} chars):\n")
            f.write("-" * 40 + "\n")
            f.write(chunk + "\n")
            f.write("-" * 40 + "\n")
        
        # Check for overlap between consecutive chunks
        if len(chunks) > 1:
            f.write("\n\nOVERLAP ANALYSIS:\n")
            f.write("=" * 50 + "\n")
            
            for i in range(1, len(chunks)):
                # Find overlap between chunks
                prev_chunk = chunks[i-1]
                curr_chunk = chunks[i]
                
                # Check end of previous chunk against start of current chunk
                overlap_found = False
                for j in range(1, min(len(prev_chunk), len(curr_chunk))):
                    if curr_chunk.startswith(prev_chunk[-j:]):
                        f.write(f"Overlap between chunks {i} and {i+1}: {prev_chunk[-j:]}\n")
                        overlap_found = True
                        break
                
                if not overlap_found:
                    f.write(f"No direct text overlap found between chunks {i} and {i+1}\n")
    
    # Print a simple summary to console
    print(f"Processed {pdf_path}")
    print(f"Number of chunks created: {len(chunks)}")
    print(f"Chunks saved to: {output_file}")
    
    return chunks, output_file

# Run the test with your PDF file
if _name_ == "_main_":
    # Replace with the path to your PDF file
    pdf_file_path = "/Users/jyothi/Desktop/rag_pipeline_capstone2/capstone-2/constitutionofindiaacts.pdf"
    
    # You can optionally specify an output file path as the second argument
    # chunks, output_file = test_chunking_service_with_pdf(pdf_file_path, "custom_output_file.txt")
    
    # Or let the function automatically generate an output filename
    chunks, output_file = test_chunking_service_with_pdf(pdf_file_path)