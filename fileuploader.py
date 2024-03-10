import streamlit as st
import embeddings  

def fileuploader_callback():
    print( st.session_state)


uploaded_vectors = embeddings.getUploadedFiles()



st.title("Upload PDF🤖")

uploaded_files = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    # Temporary saving uploaded file to process it
    with open("temp_file.pdf", "wb") as f:
        f.write(uploaded_file.getvalue())

    # Process the PDF
    texts = embeddings.process_pdf("temp_file.pdf")

    # Create embeddings
    embeddingsList = embeddings.create_embeddings(texts)

    # Upsert embeddings to Pinecone
    uploaded_vectors = embeddings.upsert_embeddings_to_pinecone(embeddingsList, uploaded_file.name)
 

st.subheader("Uploaded documents 📚")
for vector in uploaded_vectors:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(vector)
    with col2:
        if st.button("Delete", key=vector):
            embeddings.deleteNamespace(vector)
            st.rerun()

