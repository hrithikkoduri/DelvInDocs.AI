from langchain.text_splitter import SpacyTextSplitter
from langchain.docstore.document import Document

class TextSplitterDocLoader:
    def __init__(self, texts):
        self.texts = texts

    def pre_split_text(self, text, max_length=900000):
        return [text[i:i+max_length] for i in range(0, len(text), max_length)]

    def split_texts_load_docs(self):
        # Split the text using SpacyTextSplitter
        splitter = SpacyTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
        )
        splitted_texts = []
        for text in self.texts:
            
            # Pre-split the text if it's too long
            pre_split = self.pre_split_text(text)
            for chunk in pre_split:

                # Split each pre-split chunk individually and extend the results to the splitted_texts list
                splitted_texts.extend(splitter.split_text(chunk))
        
        # Create Document objects for each splitted text
        docs = [Document(page_content=text) for text in splitted_texts]
        
        print(f"Created {len(docs)} documents")

        return docs