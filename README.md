# 📄 PDF Embedding Uploader 🚀

PDF Embedding Uploader is a tool that automates the process of extracting text from PDF files, generating embeddings using OpenAI's Text Embedding model, and uploading them to Pinecone for efficient similarity search.

<img width="1196" alt="Screenshot 2024-03-13 at 07 23 52" src="https://github.com/adamalmqvist/pinecone-pdf-embedder/assets/70197981/32ab536d-f159-405f-9a43-0f71a36700be">


## 🚀 Getting Started

To get started with PDF Embedding Uploader locally, follow these steps:

### Prerequisites

- Python 3.6+
- pip

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/pdf-embedding-uploader.git
    ```

2. Navigate to the project directory:

    ```bash
    cd pdf-embedding-uploader
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your OpenAI and Pinecone API keys. Replace `YOUR_OPENAI_API_KEY` and `YOUR_PINECONE_API_KEY` in the `backend.py` file with your actual API keys.

### Usage

1. Run the Streamlit frontend:

    ```bash
    streamlit run frontend.py
    ```

2. Upload a PDF file using the provided file uploader.

3. Wait for the embeddings to be processed and uploaded to Pinecone.

4. Once the process is complete, you will see a list of uploaded PDFs with their corresponding embeddings.

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

If you encounter any issues or have suggestions for improvements, please [open an issue](https://github.com/yourusername/pdf-embedding-uploader/issues).

