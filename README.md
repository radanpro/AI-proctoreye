# AI ProctorEye

AI ProctorEye is an intelligent system designed to verify student identities, monitor their behavior during exams, and ensure a secure and fair examination environment. The project leverages AI techniques such as face recognition, barcode scanning, and behavior analysis to detect suspicious activity and prevent cheating.

## Features

- **Student Identity Verification**: Matches a student's current image with the one stored in the database using barcode information.
- **Exam Seat Verification**: Confirms that the student is seated in the correct location.
- **Behavior Monitoring**: Analyzes student behavior during the exam to detect cheating attempts.
- **Progressive Steps**: The project is structured in steps, where each step builds on the previous one to gradually enhance the system's capabilities.

## Project Structure

The project is divided into two main parts:

1. **Real Project** (Python-based API):
    - Contains the core functionality of student identity verification and behavior monitoring.
    - Developed using Python and organized into steps for incremental development.
  
2. **Mock Project** (Frontend with Virtual Database):
    - Contains a mock frontend with virtual data for testing and experimenting during development.

### Directory Structure

```bash
AI-proctoreye/
│
├── api/                    # Core system and API
│   ├── models/             # Core classes (Student, ImageProcessor, etc.)
│   ├── services/           # Services for identity and behavior analysis
│   ├── controllers/        # API controllers for handling requests
│   ├── utils/              # Utility functions (database, image handling)
│   ├── api_server.py       # API server entry point
│   └── requirements.txt    # Dependencies for the project
│
├── frontend/               # Mock project for UI and testing
│   ├── mock_db/            # Mock database for testing
│   ├── ui/                 # Frontend HTML/CSS files
│   └── app.js              # Frontend logic
│
└── README.md               # Project documentation
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/abdulrahmanRadan/AI-proctoreye.git
```

2. Navigate to the project directory:

```bash
cd AI-proctoreye
```

3. Install Python dependencies:

```bash
pip install -r api/requirements.txt
```

## Usage

1. Run the API server:

```bash
python api/api_server.py
```

2. Access the mock frontend to test the system's features during development.

## Development Steps

1. **Step 1**: Create an algorithm to compare the current student's image with the stored one using the barcode.
2. **Step 2**: Identify the student by comparing their image with all students stored in the database, starting with those taking the exam at the same time.
3. **Step 3**: Verify the student is seated in the correct location by matching their image with the expected student for that seat.
4. **Step 4**: Monitor student behavior and detect cheating during the exam.

## Future Improvements

- Implement live video analysis for real-time behavior monitoring.
- Add scalability to handle larger datasets and more students efficiently.
- Integrate with external exam management systems for seamless operation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
