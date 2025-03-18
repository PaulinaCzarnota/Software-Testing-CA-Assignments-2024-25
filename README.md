This repository contains my CA assignments from the Software Testing module, completed during my third year of Computer Science studies at TU Dublin. 

# Assignment 1: Unit Testing for TunePal API

This assignment focuses on unit testing the backend of the TunePal music library API. The goal was to ensure the correctness and reliability of key functionalities by implementing unit tests using Python's `unittest` and `pytest` frameworks, along with coverage analysis for test completeness.  

### Key Features Tested:

- Adding songs while preventing duplicates  
- Pagination (retrieving songs by pages)  
- Searching by title, artist, and handling special characters  
- Filtering songs by release year  
- Handling invalid inputs and preventing crashes  
- Performance validation (ensuring API response time ≤ 200ms)  
- Code quality check using `pylint`  

### Defects Identified & Fixes Implemented:

- Fixed incorrect usage of `.add()` instead of `.append()` in `add_song()`  
- Corrected page index update errors in `next_page()` and `previous_page()`  
- Ensured search functionality considers both title and artist fields  
- Addressed incorrect string-based year comparison by converting values to integers  
- Implemented duplicate song prevention before insertion  

### Unit Test Execution & Results:

The unit tests were executed in Visual Studio Code using `unittest` and `pytest`. All test cases passed successfully, confirming the correct functionality of the API. Coverage reports showed 100% code coverage, ensuring all critical functionalities were tested.  

### Commands Used for Testing:

- Running all unit tests:  
  ```sh
  python -m unittest discover
  ```
- Running a specific test file:  
  ```sh
  python -m unittest test_tunepalapi.py
  ```
- Running tests with coverage tracking:  
  ```sh
  coverage run -m unittest discover
  coverage report -m
  ```
- Checking code quality:  
  ```sh
  pylint tunepalapi.py test_tunepalapi.py
  ```  

### System Requirements & Development Plan:
The TunePal system requirements define user functionalities such as song searching, account management, and premium song purchases. The development plan follows an Agile Scrum methodology, integrating unit testing throughout the software development lifecycle to ensure quality and stability before deployment.  

This unit testing assignment successfully validates the TunePal API's functionality and prepares it for integration with the front-end application.
