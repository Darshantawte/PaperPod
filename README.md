# PaperPod

Convert documents (PDF, DOCX) into podcasts with AI-powered summarization.

## Features

- Upload PDF and DOCX files
- AI-powered document summarization
- Text-to-Speech conversion
- Progress tracking
- Responsive UI
- Docker support

## Tech Stack

- Python/Flask
- Transformers (BART) for summarization
- gTTS for text-to-speech
- Docker for containerization

## Installation

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/paperpod.git
cd paperpod
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create .env file:

```bash
cp .env.example .env
```

5. Run the application:

```bash
python app.py
```

### Docker Setup

1. Build and run using Docker Compose:

```bash
docker-compose up --build
```

2. Access the application at `http://localhost:5000`

## Usage

1. Open the application in your web browser
2. Upload a PDF or DOCX file
3. Wait for the processing to complete
4. Listen to the generated podcast
