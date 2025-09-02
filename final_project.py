import os

# Global dictionary to store all student data
students_data = {}

def display_menu():
    """Displays the main menu with formatted layout"""
    # Using string multiplication for consistent formatting
    print("\n" + "=" * 50)
    print(" " * 10 + "Student Records Management System")
    print("=" * 50)
    print(" " * 10 + "1. Add Student")
    print(" " * 10 + "2. Update Grade")
    print(" " * 10 + "3. Search Student Record")
    print(" " * 10 + "4. Delete Student Record")
    print(" " * 10 + "5. Calculate Average Grade")
    print(" " * 10 + "6. Generate Report")
    print(" " * 10 + "7. Exit")
    print("=" * 50)

def press_enter_to_continue():
    """Helper function to pause execution and wait for user input"""
    input("" \
    "...")

def load_students(filename):
    """
    Loads student data from a file into global students_data dictionary
    Args:
        filename (str): The name of the file containing student data
    """
    global students_data
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    # Split line into parts: ID, name, then grade entries
                    parts = line.split(',')
                    student_id = parts[0]
                    student_name = parts[1]
                    grades = {}
                    
                    # Process each grade entry (format: subject:grade)
                    for grade_entry in parts[2:]:
                        if ':' in grade_entry:
                            subject, grade = grade_entry.split(':', 1)
                            try:
                                # Convert grade to integer and store in grades dict
                                grades[subject] = int(grade)
                            except ValueError:
                                # Skip invalid grade entries but keep the rest
                                print(f"Invalid grade for {student_id} in {subject}. Skipping")
                    # Store student data in global dictionary
                    students_data[student_id] = {'name': student_name, 'grades': grades}
        print("\nStudent data loaded successfully.\n")
    except FileNotFoundError:
        print(f"\nFile {filename} not found. Starting with empty data.")
        students_data = {}
    except Exception as e:
        print(f"Error loading data from file: {e}")

def save_students(students_data, filename):
    """
    Saves student data from dictionary to file
    Args:
        students_data (dict): Dictionary containing all student data
        filename (str): The name of the file to save data to
    """
    try:
        with open(filename, 'w') as file:
            for student_id, info in students_data.items():
                # Convert grades dictionary to comma-separated string
                grades_str = ','.join([f"{subject}:{grade}" for subject, grade in info['grades'].items()])
                # Write student record in format: ID,name,subject1:grade1,subject2:grade2...
                file.write(f"{student_id},{info['name']},{grades_str}\n")
        print("\nData saved successfully.\n")
    except IOError as e:
        print(f"Error saving data: {e}")

def add_student(students_data):
    """
    Adds a new student to the system
    Args:
        students_data (dict): Dictionary containing all student data
    Returns:
        bool: True if student was successfully added, False otherwise
    """
    print("\nAdd New Student")
    try: 
        student_id = input("Enter Student ID: ").strip()
        # Validate ID input
        if not student_id:
            print("Student ID cannot be empty.")
            return False
        if not student_id.isdigit():
            raise ValueError("Invalid input. Student ID must be an integer.")
        if student_id in students_data:
            print("Student ID already exists. Please try again.")
            return False
            
        student_name = input("Enter Student Name: ").strip()
        # Validate name inpu t
        if not student_name:
            print("Student Name cannot be empty.")
            return False
        if student_name.isdigit():
            print("Enter a valid student name.")
            return False
            
        # Add student to dictionary with empty grades
        students_data[student_id] = {'name': student_name, 'grades': {}}
        print(f"Student '{student_name}' added successfully.")
        return True
    except ValueError as e:
        print(f"Error: {e} Please enter valid input.")
        return False

def update_grade(students_data):
    """
    Updates or adds a grade for specific student and subject
    Args:
        students_data (dict): Dictionary containing all student data
    Returns:
        bool: True if grade was successfully updated, False otherwise
    """
    print("\nUpdate Student Grade")
    student_id = input("Enter Student ID: ").strip()
    # Verify student exists
    if student_id not in students_data:
        print("Student not found.")
        return False
        
    subject = input("Enter Subject Name: ").strip()
    # Validate subject input
    if not subject:
        print("Subject name cannot be empty.")
        return False
    if subject.isdigit():
        print("Enter a valid subject name.")
        return False
        
    new_grade = input("Enter New Grade (0-100): ").strip()
    try:
        # Validate and convert grade input
        new_grade_float = float(new_grade)
        new_grade_int = int(new_grade_float)
        if new_grade_int < 0 or new_grade_int > 100:
            print("Grade must be between 0 and 100.")
            return False
    except ValueError:
        print("Invalid grade input. Please enter a numeric value.")
        return False
        
    # Update the grade in the student's record
    students_data[student_id]['grades'][subject] = new_grade_int
    print(f"Grade updated for {students_data[student_id]['name']} in {subject}.")
    return True

def search_student_records(students_data):
    """
    Searches for student records by ID and displays detailed information
    Args:
        students_data (dict): Dictionary containing all student data
    """
    print("\nSearch Student Records")
    if not students_data:
        print("No students to search.")
        return
        
    search_term = input("Enter Student ID to search: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return
        
    # Find matching students
    matches = []
    for student_id, info in students_data.items():
        if search_term == student_id:
            matches.append((student_id, info))
            
    # Display results
    if matches:
        print(f"\nFound {len(matches)} matching student(s):")
        print("-" * 70)
        for sid, info in matches:
            grades = info['grades']
            # Calculate average if grades exist
            average = sum(grades.values()) / len(grades) if grades else 0
            # Create formatted string of all grades
            grades_str = ', '.join([f"{subject}: {grade}" for subject, grade in grades.items()]) if grades else "No grades"
            print(f"ID: {sid}\nName: {info['name']}\nGrades: {grades_str}\nAverage: {average:.2f}\n{'-'*70}")
        print()
    else:
        print("No matching students found.")

def delete_student_record(students_data):
    """
    Deletes a student record after confirmation
    Args:
        students_data (dict): Dictionary containing all student data
    Returns:
        bool: True if student was deleted, False if operation was cancelled
    """
    print("\nDelete Student Record")
    if not students_data:
        print("No students to delete.")
        return False
        
    student_id_input = input("Enter Student ID to delete: ").strip()
    
    # Find matching student
    matched_id = None
    for student_id in students_data:
        if student_id == student_id_input:
            matched_id = student_id
            break
            
    if not matched_id:
        print("Student not found.")
        return False
        
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete student '{students_data[matched_id]['name']}' (ID: {matched_id})? (y/n): ").strip().lower()
    if confirm == 'y':
        del students_data[matched_id]
        print("Student record deleted successfully.")
        return True
    else:
        print("Deletion cancelled.")
        return False

def calculate_average_grade(students_data):
    """
    Calculates and displays average grade for student or subject
    Args:
        students_data (dict): Dictionary containing all student data
    """
    print("\nCalculate Average Grade")
    choice = input("Calculate average for (student/subject): ").strip().lower()
    
    if choice == 'student':
        student_id = input("Enter Student ID: ").strip()
        if not student_id:
            print("Please enter student ID.")
            return
        if student_id not in students_data:
            print("Student not found.")
            return
            
        grades = students_data[student_id]['grades'].values()
        if grades:
            average = sum(grades) / len(grades)
            print(f"Average grade for {students_data[student_id]['name']}: {average:.2f}")
        else:
            print("No grades available for this student.")
            
    elif choice == 'subject':
        subject = input("Enter Subject Name: ").strip().lower()
        if not subject:
            print("Please enter the subject name.")
            return
            
        total, count = 0, 0
        # Calculate average across all students for the subject
        for student in students_data.values():
            for student_subject in student['grades']:
                if student_subject.lower() == subject: 
                    total += student['grades'][student_subject]
                    count += 1
                    
        if count > 0:
            average = total / count
            print(f"Average grade for {subject}: {average:.2f}")
        else:
            print("No grades available for this subject.")
    else:
        print("Invalid choice. Please enter 'student' or 'subject'.")

def generate_report(students_data):
    """
    Generates a detailed report of all students and their grades
    Args:
        students_data (dict): Dictionary containing all student data
    """
    if not students_data:
        print("\nNo students to display.\n")
        return
        
    print("\nStudent Report:")
    print("-" * 70)
    for student_id, info in students_data.items():
        grades = info['grades']
        # Calculate average if grades exist
        average = sum(grades.values()) / len(grades) if grades else 0
        # Create formatted string of all grades
        grades_str = ', '.join([f"{subject}: {grade}" for subject, grade in grades.items()]) if grades else "No grades"
        print(f"ID: {student_id}\nName: {info['name']}\nGrades: {grades_str}\nAverage: {average:.2f}\n{'-'*70}")
    print()

def main_program_loop():
    """
    Main program loop that handles menu navigation and function calls
    """
    # Load existing data at startup
    load_students("grades.txt")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            # Add student and save if successful
            if add_student(students_data):
                save_students(students_data, "grades.txt")
            press_enter_to_continue()
        elif choice == '2':
            # Update grade and save if successful
            if update_grade(students_data):
                save_students(students_data, "grades.txt")
            press_enter_to_continue()
        elif choice == '3':
            search_student_records(students_data)
            press_enter_to_continue()
        elif choice == '4':
            # Delete student and save if successful
            if delete_student_record(students_data):
                save_students(students_data, "grades.txt")
            press_enter_to_continue()
        elif choice == '5':
            calculate_average_grade(students_data)
            press_enter_to_continue()
        elif choice == '6':
            generate_report(students_data)
            press_enter_to_continue()
        elif choice == '7':
            # Save data before exiting
            save_students(students_data, "grades.txt")
            print("Exiting the program. Data saved.")
            break
        else:
            print("Invalid choice. Please try again.")
            press_enter_to_continue()

# Start the program
main_program_loop()