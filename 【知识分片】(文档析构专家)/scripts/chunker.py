import os
import re
import json

class SemanticChunker:
    def __init__(self, file_path, output_dir="chunks"):
        self.file_path = file_path
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def slice_by_headers(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regular expression to catch Markdown headers
        # Matches #, ##, ###, etc.
        pattern = r'(^#+\s+.*$)'
        parts = re.split(pattern, content, flags=re.MULTILINE)
        
        chunks = []
        current_header_path = []
        
        for part in parts:
            if re.match(r'^#+', part):
                level = len(part.split()[0])
                header_text = part.strip()
                
                # Update header path
                if level <= len(current_header_path):
                    current_header_path = current_header_path[:level-1]
                current_header_path.append(header_text)
            else:
                if part.strip():
                    chunk_data = {
                        "path": " > ".join(current_header_path),
                        "content": part.strip()
                    }
                    chunks.append(chunk_data)
        
        return chunks

    def save_chunks(self, chunks):
        manifest = []
        for i, chunk in enumerate(chunks):
            filename = f"chunk_{i:03d}.json"
            full_path = os.path.join(self.output_dir, filename)
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(chunk, f, indent=2, ensure_ascii=False)
            manifest.append({"id": i, "path": chunk['path'], "file": filename})
        
        with open(os.path.join(self.output_dir, "manifest.json"), 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"✅ Successfully sliced into {len(chunks)} chunks.")

if __name__ == "__main__":
    # Test on a skill file
    chunker = SemanticChunker("/Users/neverdie/iflow_workspace/qiuzhi-skill-creator/SKILL.md")
    chunks = chunker.slice_by_headers()
    chunker.save_chunks(chunks)
