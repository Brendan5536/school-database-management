# School Database Management System

A comprehensive school database management system designed to facilitate the tracking, updating, and management of student and staff data. Built using Python, MySQL, and Flask, this application offers a dynamic web interface for users to interact with the database easily.

## Features

- **Manage Student Records:** Add, update, and delete student details.
- **Staff Management:** Keep track of staff information, including qualifications, departments, and personal details.
- **Class Assignments:** Associate students with classes and teachers to particular subjects.
- **Attendance Tracking:** Record and view attendance for both students and staff.

## Prerequisites

Requirements: 
- Python 3.x installed
- MySQL Server running locally or remotely with necessary credentials
- Flask installed in your Python environment

## Installation

To install: 

1. Clone the repository from GitHub:

```bash
git clone https://github.com/Brendan5536/school-database-management.git
```

2. Navigate to the cloned directory:

```bash
cd school-database-management
```

3. Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

4. Import the MySQL database structure and initial data from `dataManage.sql` into your MySQL server. You can do this by accessing your MySQL Command-Line Client and executing:

```sql
source path/to/dataManage.sql;
```


## Configuration

Before running the application, you must configure your database connection settings. Open the `config.py` file in your favorite editor and update the following lines with your MySQL server details:

```python
MYSQL_DATABASE_USER = 'your_mysql_username'
MYSQL_DATABASE_PASSWORD = 'your_mysql_password'
MYSQL_DATABASE_DB = 'your_database_name'
MYSQL_DATABASE_HOST = 'your_host'
```

Replace `'your_mysql_username'`, `'your_mysql_password'`, `'your_database_name'`, and `'your_host'` with your actual MySQL username, password, database name, and host, respectively.

## Running the Application

After completing the installation and configuration, you can run the application using Flask. From the project's root directory, execute:

```bash
flask run
```

By default, the flask app will run on http://127.0.0.1:5000/. 

## Usage

- **Home Page:** Navigate through the available options to manage students, staff, classes, and attendance.
- **Add New Records:** Use the forms to add new students, staff members, classes, or attendance records.
- **View and Update:** Access the list of existing records, where you can view details or choose to update or delete them.

## Contributing to the School Database Management System

To contribute to the project, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`.
4. Push to the original branch: `git push origin <project_name>/<location>`.
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Contact

If you want to contact me, you can reach me at brendan@jarmusz.com.

## License

This project uses the following license: [MIT](https://opensource.org/licenses/MIT).