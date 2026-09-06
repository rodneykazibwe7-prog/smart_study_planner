import os

FILE_NAME = "study_log.txt"


def classify_session(duration):
    """
    Classifies study session duration based on time spent.
    - Short: under 30 minutes
    - Medium: 30 to 90 minutes (inclusive)
    - Long: over 90 minutes
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def load_sessions():
    """
    Loads saved study sessions from the text file into a list of dictionaries.
    Handles the case where the file does not exist yet.
    """
    sessions = []
    if not os.path.exists(FILE_NAME):
        return sessions

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    # File format: Subject|Topic|Date|Duration
                    parts = line.split("|")
                    if len(parts) == 4:
                        subject, topic, date, duration_str = parts
                        sessions.append({
                            "subject": subject,
                            "topic": topic,
                            "date": date,
                            "duration": float(duration_str)
                        })
    except Exception as e:
        print(f"Error loading file: {e}")
    return sessions


def save_sessions(sessions):
    """
    Saves the list of session dictionaries to a text file using standard pipe delimiters.
    """
    try:
        with open(FILE_NAME, "w") as file:
            for s in sessions:
                file.write(f"{s['subject']}|{s['topic']}|{s['date']}|{s['duration']}\n")
        print("\nSessions saved successfully to 'study_log.txt'.")
    except Exception as e:
        print(f"Error saving sessions: {e}")


def add_session(sessions):
    """
    Prompts user for session details, validates duration input,
    and appends a new dictionary session to the sessions list.
    """
    print("\n--- ADD NEW STUDY SESSION ---")
    subject = input("Enter Subject Name: ").strip()
    topic = input("Enter Topic Covered: ").strip()
    date = input("Enter Date / Day Label (e.g., 2026-03-30 or Monday): ").strip()

    # Input validation for duration
    while True:
        try:
            duration = float(input("Enter Duration in minutes: "))
            if duration > 0:
                break
            else:
                print("Duration must be a positive number greater than 0. Try again.")
        except ValueError:
            print("Invalid input! Please enter a numerical value for duration.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }
    sessions.append(session)
    print("Study session logged successfully!")


def view_sessions(sessions):
    """
    Displays all recorded study sessions in a formatted table layout.
    """
    print("\n--- ALL STUDY SESSIONS ---")
    if not sessions:
        print("No study sessions logged yet.")
        return

    # Table Header
    print(f"{'Subject':<18} | {'Topic':<22} | {'Date':<12} | {'Duration (min)':<14} | {'Category'}")
    print("-" * 80)

    for s in sessions:
        category = classify_session(s["duration"])
        print(f"{s['subject']:<18} | {s['topic']:<22} | {s['date']:<12} | {s['duration']:<14.1f} | {category}")


def search_by_subject(sessions):
    """
    Searches and prints sessions matching a specific subject (case-insensitive)
    along with total minutes/hours spent on that subject.
    """
    print("\n--- SEARCH SESSIONS BY SUBJECT ---")
    if not sessions:
        print("No study sessions recorded to search.")
        return

    query = input("Enter Subject Name to search: ").strip().lower()
    matching_sessions = [s for s in sessions if s["subject"].lower() == query]

    if not matching_sessions:
        print(f"No study sessions found for '{query}'.")
        return

    print(f"\nFound {len(matching_sessions)} session(s) for '{query.title()}':\n")
    print(f"{'Subject':<18} | {'Topic':<22} | {'Date':<12} | {'Duration (min)':<14} | {'Category'}")
    print("-" * 80)

    total_duration = 0
    for s in matching_sessions:
        category = classify_session(s["duration"])
        total_duration += s["duration"]
        print(f"{s['subject']:<18} | {s['topic']:<22} | {s['date']:<12} | {s['duration']:<14.1f} | {category}")

    total_hours = total_duration / 60
    print("-" * 80)
    print(f"Total time spent on {query.title()}: {total_duration:.1f} min ({total_hours:.2f} hrs)")


def study_statistics(sessions):
    """
    Computes overall total hours, total hours per subject, weakest subject,
    and single longest study session.
    """
    print("\n--- STUDY STATISTICS & ANALYSIS ---")
    if not sessions:
        print("No study sessions recorded yet to generate statistics.")
        return

    # Overall total study hours
    total_minutes = sum(s["duration"] for s in sessions)
    total_hours = total_minutes / 60

    # Total hours per subject calculation
    subject_totals = {}
    for s in sessions:
        subj = s["subject"].title()  # Normalize case for display
        subject_totals[subj] = subject_totals.get(subj, 0) + s["duration"]

    # Subject with least total study time
    weakest_subject = min(subject_totals, key=subject_totals.get)

    # Single longest session
    longest_session = max(sessions, key=lambda s: s["duration"])

    print(f"1. Total Hours Studied Overall: {total_hours:.2f} hrs ({total_minutes:.1f} mins)")
    print("\n2. Total Time Studied Per Subject:")
    for subj, mins in subject_totals.items():
        print(f"   - {subj}: {mins / 60:.2f} hrs ({mins:.1f} mins)")

    print(f"\n3. Weakest Subject (Least Time Spent): {weakest_subject} ({subject_totals[weakest_subject] / 60:.2f} hrs)")
    
    longest_cat = classify_session(longest_session['duration'])
    print("\n4. Single Longest Session Recorded:")
    print(f"   Subject:  {longest_session['subject']}")
    print(f"   Topic:    {longest_session['topic']}")
    print(f"   Date:     {longest_session['date']}")
    print(f"   Duration: {longest_session['duration']:.1f} min ({longest_cat})")


def main():
    """
    Main loop providing a menu-driven interface.
    """
    sessions = load_sessions()

    while True:
        print("\n=================================")
        print("     SMART STUDY PLANNER")
        print("=================================")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        print("=================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Thank you for using Smart Study Planner. Goodbye!")
            break
        else:
            print("Invalid selection! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()