import sys
import os

def load_schools(filename="SC.TXT"):
    """
    Loads school data from the specified file.
    Each line should be in the format: code;name;days_per_cycle;lessons_per_day
    Returns a dictionary of school data, keyed by school code.
    """
    if not os.path.exists(filename):
        print(f"Error: School data file '{filename}' not found.")
        return None
    
    schools = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) == 4:
                    code, name, days, lessons = parts
                    schools[code] = {
                        "name": name,
                        "days_per_cycle": int(days),
                        "lessons_per_day": int(lessons)
                    }
    except Exception as e:
        print(f"Error reading school file: {e}")
        return None
    return schools

def load_teacher_data(filename, school_info):
    """
    Loads teacher timetables and substitution counts from a file.
    Validates the data against the selected school's configuration.
    Returns a list of teacher dictionaries and a set of all class codes.
    """
    if not os.path.exists(filename):
        print(f"Error: Timetable file '{filename}' not found.")
        return None, None
        
    teachers = []
    all_class_codes = set()
    
    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                parts = line.strip().split(';')
                
                # Validate number of parts: code;n_subs;day1;day2;...
                expected_parts = 2 + school_info['days_per_cycle']
                if len(parts) != expected_parts:
                    print(f"Error in {filename} on line {line_num}: Incorrect number of fields.")
                    print(f"Expected {expected_parts} fields, but found {len(parts)}.")
                    return None, None

                teacher_code = parts[0]
                n_subs = int(parts[1])
                timetable = parts[2:]

                # Validate timetable data consistency
                for day_data in timetable:
                    if len(day_data) != school_info['lessons_per_day']:
                        print(f"Error in {filename} for teacher {teacher_code}:")
                        print(f"Lesson data '{day_data}' has length {len(day_data)}, but school expects {school_info['lessons_per_day']} lessons per day.")
                        return None, None
                    
                    # Collect class codes
                    for lesson_code in day_data:
                        if lesson_code != '#':
                            all_class_codes.add(lesson_code)

                teachers.append({
                    "code": teacher_code,
                    "n_subs": n_subs,
                    "timetable": timetable
                })
    except ValueError:
        print(f"Error: Non-integer value found for substitution count in '{filename}'.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred while reading '{filename}': {e}")
        return None, None

    return teachers, sorted(list(all_class_codes))

def find_substitute(absent_teacher, day_index, lesson_index, all_teachers):
    """
    Finds the best substitute teacher based on the 4-step criteria.
    """
    # Step 1: Find all available teachers
    available_teachers = [
        t for t in all_teachers 
        if t['code'] != absent_teacher['code'] and t['timetable'][day_index][lesson_index] == '#'
    ]

    if not available_teachers:
        return None

    # If only one is available, they are the choice.
    if len(available_teachers) == 1:
        return available_teachers[0]

    # Step 2: Find teacher(s) with the smallest N
    min_n = min(t['n_subs'] for t in available_teachers)
    candidates_step2 = [t for t in available_teachers if t['n_subs'] == min_n]

    if len(candidates_step2) == 1:
        return candidates_step2[0]

    # Step 3: Find teacher(s) with the fewest teaching lessons on that day
    min_lessons_on_day = float('inf')
    candidates_step3 = []
    
    for teacher in candidates_step2:
        lessons_on_day = sum(1 for lesson in teacher['timetable'][day_index] if lesson != '#')
        if lessons_on_day < min_lessons_on_day:
            min_lessons_on_day = lessons_on_day
            candidates_step3 = [teacher]
        elif lessons_on_day == min_lessons_on_day:
            candidates_step3.append(teacher)

    if len(candidates_step3) == 1:
        return candidates_step3[0]

    # Step 4: Find teacher with the smallest code alphabetically
    candidates_step3.sort(key=lambda t: t['code'])
    return candidates_step3[0]
    
def get_teacher_by_code(code, teachers):
    """Utility to find a teacher dictionary by their code."""
    return next((t for t in teachers if t['code'] == code), None)

def update_data_file(filename, teachers):
    """Saves the updated teacher data back to the file."""
    try:
        with open(filename, 'w') as f:
            for teacher in teachers:
                timetable_str = ";".join(teacher['timetable'])
                f.write(f"{teacher['code']};{teacher['n_subs']};{timetable_str}\n")
    except Exception as e:
        print(f"\nError: Could not write updates to {filename}. {e}")

def generate_output_file(school_name, absent_teacher_code, day, final_subs):
    """Generates the OUTPUT.TXT file with the substitution details."""
    try:
        with open("OUTPUT.TXT", 'w') as f:
            f.write(f"Name of school: {school_name}\n")
            f.write(f"Substitution for {absent_teacher_code} on Day {day}\n\n")
            
            # Write headers
            f.write(f"{'Lesson':<10}{'Class':<10}{'Substitute':<10}\n")
            f.write(f"{'-'*8:<10}{'-'*8:<10}{'-'*8:<10}\n")
            
            # Write data sorted by lesson number
            for lesson_num in sorted(final_subs.keys()):
                sub_info = final_subs[lesson_num]
                f.write(f"{lesson_num:<10}{sub_info['class']:<10}{sub_info['substitute_code']:<10}\n")
        print("\nSuccessfully generated substitution form 'OUTPUT.TXT'.")
    except Exception as e:
        print(f"\nError: Could not write to OUTPUT.TXT. {e}")


def main():
    """Main function to run the lesson substitution program."""
    print("--- Lesson Substitution Program ---")

    # 1. Load Schools
    schools = load_schools()
    if schools is None:
        sys.exit()

    # 2. Select School
    selected_school = None
    while True:
        school_code = input("\nEnter school code (or 'quit' to exit): ").strip()
        if school_code.lower() == 'quit':
            sys.exit()
        
        if school_code in schools:
            selected_school = schools[school_code]
            print(f"\nSchool Name: {selected_school['name']}")
            print(f"Days per cycle: {selected_school['days_per_cycle']}")
            print(f"Lessons per day: {selected_school['lessons_per_day']}")
            
            confirm = input("Confirm this is the correct school? (y/n): ").lower().strip()
            if confirm == 'y':
                break
        else:
            print("Invalid school code. Please try again.")

    # 3. Load Timetable Data
    timetable_filename = input("\nEnter the name of the timetable data file (e.g., ABC_data.txt): ").strip()
    teachers, class_codes = load_teacher_data(timetable_filename, selected_school)
    
    if teachers is None:
        print("Program terminated due to data mismatch.")
        sys.exit()

    print("\nData loaded successfully.")
    print(f"Teacher Codes Found: {', '.join(t['code'] for t in teachers)}")
    print(f"Class Codes Found: {', '.join(class_codes)}")
    
    confirm = input("Does this information seem correct? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Please check the input file. Program terminated.")
        sys.exit()

    # 4. Get Substitution Details
    while True:
        try:
            day = int(input("\nEnter day of cycle for substitution: ").strip())
            if 1 <= day <= selected_school['days_per_cycle']:
                day_index = day - 1
                break
            else:
                print(f"Invalid day. Please enter a number between 1 and {selected_school['days_per_cycle']}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    absent_teacher = None
    while not absent_teacher:
        absent_teacher_code = input("Enter code of teacher who needs substitution: ").strip().upper()
        absent_teacher = get_teacher_by_code(absent_teacher_code, teachers)
        if not absent_teacher:
            print("Teacher code not found. Please try again.")

    # 5. Find Substitutions
    lessons_to_sub = []
    absent_timetable_for_day = absent_teacher['timetable'][day_index]
    for i, class_code in enumerate(absent_timetable_for_day):
        if class_code != '#':
            lessons_to_sub.append({'lesson_index': i, 'class': class_code})
            
    if not lessons_to_sub:
        print(f"\n{absent_teacher_code} has no lessons on Day {day}. No substitution needed.")
        sys.exit()

    print("\nFinding substitute teachers...")
    suggestions = {}
    for lesson in lessons_to_sub:
        lesson_index = lesson['lesson_index']
        suggestion = find_substitute(absent_teacher, day_index, lesson_index, teachers)
        suggestions[lesson_index] = suggestion

    # 6. Display and Confirm Suggestions
    print("\n--- Substitution Suggestions ---")
    print(f"For {absent_teacher_code} on Day {day}:\n")
    for lesson in lessons_to_sub:
        idx = lesson['lesson_index']
        class_code = lesson['class']
        suggestion = suggestions.get(idx)
        sug_code = suggestion['code'] if suggestion else "== NO ONE AVAILABLE =="
        print(f"  Lesson {idx + 1} (Class {class_code}): --> Suggestion: {sug_code}")
    
    print("\n--- Confirm or Override ---")
    final_substitutions = {}
    for lesson in lessons_to_sub:
        lesson_index = lesson['lesson_index']
        suggested_teacher = suggestions.get(lesson_index)
        
        if not suggested_teacher:
            print(f"Lesson {lesson_index + 1}: No substitute was found. Skipping.")
            continue

        while True:
            prompt = f"Lesson {lesson_index+1} (Class {lesson['class']}) - Accept {suggested_teacher['code']}? (y/override_code): "
            choice = input(prompt).strip().upper()

            if choice == 'Y':
                final_substitutions[lesson_index + 1] = {
                    "substitute_code": suggested_teacher['code'],
                    "class": lesson['class']
                }
                break
            elif choice: # User provided an override code
                override_teacher = get_teacher_by_code(choice, teachers)
                if not override_teacher:
                    print("Invalid override teacher code.")
                elif override_teacher['code'] == absent_teacher_code:
                    print("The absent teacher cannot substitute for themselves.")
                elif override_teacher['timetable'][day_index][lesson_index] != '#':
                    print(f"Teacher {choice} is not free for Lesson {lesson_index + 1}.")
                else:
                    final_substitutions[lesson_index + 1] = {
                        "substitute_code": override_teacher['code'],
                        "class": lesson['class']
                    }
                    print(f"Override accepted: {choice} for Lesson {lesson_index + 1}.")
                    break
            else:
                print("Invalid input. Please enter 'y' or a valid teacher code.")

    # 7. Finalize and Update
    if not final_substitutions:
        print("\nNo substitutions were confirmed. Exiting.")
        sys.exit()

    # Update N values
    absent_teacher['n_subs'] -= len(lessons_to_sub)
    for sub_info in final_substitutions.values():
        substitute = get_teacher_by_code(sub_info['substitute_code'], teachers)
        if substitute:
            substitute['n_subs'] += 1

    print("\nUpdating teacher data file...")
    update_data_file(timetable_filename, teachers)
    
    # Generate OUTPUT.TXT
    generate_output_file(selected_school['name'], absent_teacher_code, day, final_substitutions)

    print("\nProgram finished successfully.")


if __name__ == "__main__":
    main()
