# Lingosense

This project detects the language of a message, translates it to English, and classifies the intent like complaint, order, query, etc. using NLP.
It supports typed input, PDF/Word file uploads, and is ready to expand to speech input in future.

 Features

- Language Detection – Detects over 50 languages.
- Auto-Translation – Converts messages into English using Google Translate.
- Intent Classification – Uses a BERT-based model to classify intent.
- File Upload Support – Upload pdf or docx files and analyze their content.
- Modern UI – Clean frontend built with HTML, CSS, JavaScript.
- Flask Backend– REST API for real-time interaction.

Tech Stack

 Frontend      HTML, CSS, JavaScript          
 Backend       Python Flask                   
 NLP Models    HuggingFace Transformers (BERT)
 Language API  LangDetect + Googletrans       
 File Support  PyMuPDF, python-docx           

Project Structure

multilingual-intent-api/
├── app.py
├── requirements.txt
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── uploads/
├── README.md
└── .gitignore
