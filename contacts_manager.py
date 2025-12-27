import json
import re
from datetime import datetime
import csv
import os

FILE_NAME = "contacts_data.json"

# ---------------- VALIDATIONS ----------------
def validate_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ---------------- FILE HANDLING ----------------
def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    print("\n✅ No existing contacts file found. Starting fresh.\n")
    return {}

def save_contacts(contacts):
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)
    print("✅ Contacts saved to contacts_data.json")

# ---------------- CORE FUNCTIONS ----------------
def add_contact(contacts):
    print("\n--- ADD NEW CONTACT ---")

    while True:
        name = input("Enter contact name: ").strip()
        if name:
            break
        print("Name cannot be empty!")

    while True:
        phone = input("Enter phone number: ").strip()
        valid, cleaned = validate_phone(phone)
        if valid:
            break
        print("Invalid phone number!")

    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip()
        if not email or validate_email(email):
            break
        print("Invalid email format!")

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"

    contacts[name] = {
        "phone": cleaned,
        "email": email if email else None,
        "address": address if address else None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    print(f"✅ Contact '{name}' added successfully!")
    save_contacts(contacts)

def view_all_contacts(contacts):
    print(f"\n--- ALL CONTACTS ({len(contacts)} total) ---")
    print("=" * 60)

    if not contacts:
        print("No contacts available.")
        return

    for name, info in contacts.items():
        print(f"👤 {name}")
        print(f"   📞 {info['phone']}")
        if info['email']:
            print(f"   📧 {info['email']}")
        print(f"   👥 {info['group']}")
        print("-" * 40)

def search_contact(contacts):
    term = input("Enter name to search: ").lower()
    results = {}

    for name, info in contacts.items():
        if term in name.lower():
            results[name] = info

    if not results:
        print("No contacts found.")
        return

    print(f"\nFound {len(results)} contact(s):")
    print("-" * 50)

    for i, (name, info) in enumerate(results.items(), 1):
        print(f"{i}. {name}")
        print(f"   📞 Phone: {info['phone']}")
        if info['email']:
            print(f"   📧 Email: {info['email']}")
        if info['address']:
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info['group']}")
        print()

def update_contact(contacts):
    name = input("Enter contact name to update: ").strip()
    if name not in contacts:
        print("Contact not found!")
        return

    print("Leave blank to keep existing value.")

    phone = input("New phone number: ").strip()
    if phone:
        valid, cleaned = validate_phone(phone)
        if valid:
            contacts[name]["phone"] = cleaned

    email = input("New email: ").strip()
    if email and validate_email(email):
        contacts[name]["email"] = email

    address = input("New address: ").strip()
    if address:
        contacts[name]["address"] = address

    group = input("New group: ").strip()
    if group:
        contacts[name]["group"] = group

    contacts[name]["updated_at"] = datetime.now().isoformat()
    print("✅ Contact updated successfully!")
    save_contacts(contacts)

def delete_contact(contacts):
    name = input("Enter contact name to delete: ").strip()
    if name in contacts:
        del contacts[name]
        print("✅ Contact deleted!")
        save_contacts(contacts)
    else:
        print("Contact not found!")

def export_to_csv(contacts):
    with open("contacts.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])
        for name, info in contacts.items():
            writer.writerow([name, info["phone"], info["email"], info["address"], info["group"]])
    print("✅ Contacts exported to contacts.csv")

def view_statistics(contacts):
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {len(contacts)}\n")

    groups = {}
    for info in contacts.values():
        groups[info["group"]] = groups.get(info["group"], 0) + 1

    print("Contacts by Group:")
    for g, c in groups.items():
        print(f"  {g}: {c} contact(s)")

    recent = 0
    for info in contacts.values():
        updated = datetime.fromisoformat(info["updated_at"])
        if (datetime.now() - updated).days <= 7:
            recent += 1

    print(f"\nRecently Updated (last 7 days): {recent}")

# ---------------- MAIN MENU ----------------
def main():
    print("=" * 50)
    print("      CONTACT MANAGEMENT SYSTEM")
    print("=" * 50)

    contacts = load_contacts()

    while True:
        print("\n==============================")
        print("          MAIN MENU")
        print("==============================")
        print("1. Add New Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. View All Contacts")
        print("6. Export to CSV")
        print("7. View Statistics")
        print("8. Exit")
        print("==============================")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contact(contacts)
        elif choice == "3":
            update_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            view_all_contacts(contacts)
        elif choice == "6":
            export_to_csv(contacts)
        elif choice == "7":
            view_statistics(contacts)
        elif choice == "8":
            save_contacts(contacts)
            print("\n==================================================")
            print("Thank you for using Contact Management System!")
            print("==================================================")
            break
        else:
            print("Invalid choice!")

# ✅ CORRECT ENTRY POINT (NO EXTRA SPACES)
if __name__ == "__main__":
    main()
