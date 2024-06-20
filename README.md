# MyGuruPlus

MyGuruPlus is a comprehensive e-learning platform designed to enhance the educational experience for students and educators. It provides a wide range of features to support virtual learning, including course management, interactive content, and real-time communication tools. This platform aims to create a seamless and engaging learning environment for all users.

## Features

- **Course Management**: Create, manage, and organize courses with ease.
- **Interactive Content**: Develop and share interactive learning materials.
- **Virtual Classrooms**: Conduct live classes and webinars with integrated video conferencing tools.
- **Assessments and Quizzes**: Create and manage various types of assessments and quizzes.
- **Discussion Forums**: Facilitate student discussions and peer interactions.
- **Progress Tracking**: Monitor student progress and performance through detailed analytics.
- **Resource Library**: Maintain a repository of learning resources and materials.
- **Notifications and Alerts**: Keep students and educators informed with timely notifications and alerts.

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript, React
- **Database**: PostgreSQL
- **Real-Time Communication**: WebSockets for real-time data transmission
- **APIs**: Integration with third-party APIs for enhanced functionality

## Installation and Setup

### Prerequisites

- Python 3.x
- Node.js
- npm (Node Package Manager) or yarn
- PostgreSQL

### Steps

1. **Clone the Repository**
    
    bash
    
    Copy code
    
    `git clone https://github.com/NagiPragalathan/MyGuruPlus.git
    cd MyGuruPlus` 
    
2. **Backend Setup**
    
    - Install Python dependencies:
        
        bash
        
        Copy code
        
        `pip install -r requirements.txt` 
        
    - Configure PostgreSQL database in `settings.py`.
    - Run migrations:
        
        bash
        
        Copy code
        
        `python manage.py migrate` 
        
    - Start the Django development server:
        
        bash
        
        Copy code
        
        `python manage.py runserver` 
        
3. **Frontend Setup**
    
    - Navigate to the frontend directory:
        
        bash
        
        Copy code
        
        `cd frontend` 
        
    - Install Node.js dependencies:
        
        bash
        
        Copy code
        
        `npm install` 
        
    - Start the React development server:
        
        bash
        
        Copy code
        
        `npm start` 
        
4. **Access the Platform**
    
    Open your browser and navigate to `http://localhost:3000` for the frontend and `http://localhost:8000` for the backend.
    

## Project Structure

java

Copy code

```MyGuruPlus/
├── backend/
│   ├── myguruplus/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── courses/
│   ├── users/
│   ├── assessments/
│   ├── discussions/
│   └── manage.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── styles/
├── README.md
├── requirements.txt
└── package.json
``` 

## Usage

- **Dashboard**: Access a comprehensive dashboard to manage courses, view analytics, and monitor student progress.
- **Virtual Classroom**: Conduct live classes and webinars with real-time interaction tools.
- **Assessments**: Create and administer quizzes, tests, and assignments.
- **Discussion Forums**: Facilitate student discussions and collaborative learning.
- **Resource Library**: Upload and share educational resources and materials.

## Contribution

Contributions to the MyGuruPlus project are welcome! If you would like to contribute, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://chatgpt.com/c/LICENSE) file for details.
