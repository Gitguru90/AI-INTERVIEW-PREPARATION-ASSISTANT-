# AI Interview Preparation Assistant

An AI-powered web application designed to help students prepare for technical interviews through personalised practice questions, resume analysis, and AI-generated feedback.

## 1. Project Overview

The **AI Interview Preparation Assistant** is a web-based application developed using Python and Streamlit. It uses the Groq API to support interview question generation and answer evaluation.

The application allows users to select an interview role, choose a practice mode, set a difficulty level, and practise interview questions. It aims to make interview preparation easier, more interactive, and accessible to students.

## 2. Project Objectives

- Help students prepare for technical interviews.
- Provide interview questions based on selected roles.
- Support different interview practice modes.
- Analyse uploaded resumes and extract relevant information.
- Provide AI-generated feedback on submitted answers.
- Help users identify areas where they can improve.

## 3. Key Features

### Resume Analysis
- Upload a resume for analysis.
- Extract text and relevant information from the uploaded resume.
- Support resume-based preparation.

### Interview Configuration
Users can customise their practice sessions by selecting:

- **Role:** SDE Intern, AI Engineer, or Data Analyst.
- **Interview Mode:** MCQ, Descriptive, Coding, or Mixed.
- **Difficulty:** Easy, Medium, or Hard.
- **Duration:** Select an available practice duration.

### AI Interview Practice
- Generate interview questions using AI.
- Practise questions according to the selected preferences.
- Submit answers for evaluation.

### Evaluation and Feedback
- Receive AI-generated feedback on answers.
- Understand mistakes and areas for improvement.
- Review performance after practice sessions.

### Dashboard
- View available interview progress and performance information.
- Identify strengths and topics that need more practice.

## 4. Technology Stack

| Technology | Usage |
|---|---|
| Python | Main programming language |
| Streamlit | Web application development |
| Groq API | AI question generation and answer evaluation |
| LLM | Understanding and generating responses |
| Resume Parsing Utilities | Extracting text from resumes |

## 5. System Workflow

1. The user opens the web application.
2. The user uploads a resume, if using resume-based preparation.
3. The user selects an interview role.
4. The user chooses the interview mode and difficulty.
5. The application generates interview questions using the AI service.
6. The user attempts the questions and submits answers.
7. The AI evaluates the submitted responses.
8. The application displays feedback and available performance information.

## 6. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Gitguru90/AI-INTERVIEW-PREPARATION-ASSISTANT-.git
```

### Step 2: Open the Project Folder

```bash
cd AI-INTERVIEW-PREPARATION-ASSISTANT-
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Groq API Key

Create a folder named `.streamlit` in the project directory.

Inside it, create a file named `secrets.toml` and add:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

Replace the placeholder with your own Groq API key.

**Security Note:** Never upload your API key or `secrets.toml` file to a public GitHub repository.

### Step 5: Run the Application

```bash
streamlit run Home.py
```

## 7. Live Project

**Live Application:**  
https://5vvxmsktfwhydrx7vlx7u4.streamlit.app/

**GitHub Repository:**  
https://github.com/Gitguru90/AI-INTERVIEW-PREPARATION-ASSISTANT-

## 8. Future Enhancements

The project can be improved further by adding:

- Voice-based mock interviews.
- Speech-to-text functionality.
- More interview roles and question categories.
- Detailed performance analytics.
- Personalised learning recommendations.
- Improved evaluation and follow-up questions.

## 9. Conclusion

The AI Interview Preparation Assistant demonstrates how artificial intelligence can support students in preparing for technical interviews. By combining an interactive web interface with AI-based question generation and feedback, the project provides a platform for practising interview skills and identifying areas for improvement.

## 10. Developer Information

**Developer:** Kiran Tomar  
**Course:** B.Tech – Mathematics and Computing  
**Institute:** Madhav Institute of Technology and Science, Gwalior  
**GitHub:** https://github.com/Gitguru90

---

*Developed as an academic project to explore the practical application of Artificial Intelligence in interview preparation.*
