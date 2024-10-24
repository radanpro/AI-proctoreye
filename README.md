
# AI ProctorEye

**⚠️ This project is currently under active development. Expect frequent updates and changes.**

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
│   ├──
│   └── requirements.txt    
│
├── frontend/ 
│
└── README.md               # Project documentation
```

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/abdulrahmanRadan/AI-proctoreye.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd AI-proctoreye
   ```

3. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment**:
   - On **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - On **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies**:

   After activating the virtual environment, install the required dependencies from the `requirements.txt` file:

   ```bash
   pip install -r api/requirements.txt
   ```

## Usage

1. **Run the API Server**:

   ```bash
   python api/api_server.py
   ```

2. **Access the Mock Frontend** to test the system's features during development.

## Development Steps

1. **Step 1**: Create an algorithm to compare the current student's image with the stored one using the barcode.
2. **Step 2**: Identify the student by comparing their image with all students stored in the database, starting with those taking the exam at the same time.
3. **Step 3**: Verify the student is seated in the correct location by matching their image with the expected student for that seat.
4. **Step 4**: Monitor student behavior and detect cheating during the exam.

## Future Improvements

- Implement live video analysis for real-time behavior monitoring.
- Add scalability to handle larger datasets and more students efficiently.
- Integrate with external exam management systems for seamless operation.

## Contributing

We welcome contributions to enhance the project! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m "Add new feature"`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## .gitignore

To maintain a clean and organized repository, the following items are included in the `.gitignore` file:

- Python bytecode and cache files
- Virtual environment directories
- Environment variable files
- Logs and debugging files
- SQLite databases (if used)
- Mock databases used for testing
- Node.js dependencies (if frontend uses Node.js)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
