import json
import random
import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colors
init()

# ============== DATA FILE ==============
SAVE_FILE = "tasks.json"

# ============== CUTE MESSAGES ==============
completion_messages = [
    "Yay! You did it! You're amazing! 🎉",
    "Task CRUSHED! You're literally the best 💪",
    "Done! Now come get your kiss 💋",
    "Look at you being all productive and handsome 😍",
    "Another one done! You're on fire today 🔥",
    "Wow, is it hot in here or is it just your productivity? 😏",
    "Task complete! You deserve a snack break 🍕",
    "BOOM! Done! I'm so proud of you 🥺",
    "Finished! You're my favorite human ❤️",
    "That's my man! Getting stuff DONE! 👑",
    "Completed! Now flex for me 💪😂",
    "Done! One step closer to world domination 🌍",
]

nag_messages = [
    "Heyyyy... you still haven't done this 👀",
    "This task is getting lonely... finish it! 😢",
    "Babe... this has been here for a while 😂",
    "I'm not saying I'm judging you... but 👀",
    "This task called. It misses being completed 📞",
    "Tick tock... this task is waiting for its hero 🦸",
]

welcome_messages = [
    "Welcome back, handsome! 💝",
    "Hey good looking, ready to be productive? 😘",
    "My favorite person is here! Let's get stuff done! 🚀",
    "Welcome! You look extra cute today 😍",
    "The productivity king has arrived! 👑",
]

# ============== PRIORITY SYSTEM ==============
PRIORITIES = {
    "1": {"label": "🔥 URGENT", "color": Fore.RED},
    "2": {"label": "⭐ Important", "color": Fore.YELLOW},
    "3": {"label": "🌙 Chill", "color": Fore.CYAN},
}

# ============== HELPER FUNCTIONS ==============

def load_tasks():
    """Load tasks from file"""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to file"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def clear_screen():
    """Clear the terminal"""
    os.system("cls" if os.name == "nt" else "clear")

def show_progress_bar(tasks):
    """Show a cute progress bar"""
    if not tasks:
        return
    
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    percentage = int((done / total) * 100)
    bar_length = 20
    filled = int(bar_length * done / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    if percentage == 100:
        msg = "ALL DONE! You're incredible! 🏆"
        color = Fore.GREEN
    elif percentage >= 75:
        msg = "Almost there, baby! 💪"
        color = Fore.GREEN
    elif percentage >= 50:
        msg = "Halfway! Keep going! 🚀"
        color = Fore.YELLOW
    elif percentage >= 25:
        msg = "Good start! You got this! ⭐"
        color = Fore.YELLOW
    else:
        msg = "Let's get to work, handsome! 😘"
        color = Fore.RED
    
    print(f"\n  {color}Progress: [{bar}] {percentage}% ({done}/{total})")
    print(f"  {msg}{Style.RESET_ALL}")

def show_header():
    """Show the app header"""
    print(Fore.MAGENTA + Style.BRIGHT + """
    ╔═══════════════════════════════════════╗
    ║     💝  L O V E   T A S K  💝        ║
    ║     ── Your Cute To-Do List ──        ║
    ╚═══════════════════════════════════════╝
    """ + Style.RESET_ALL)

def show_menu():
    """Show the main menu"""
    print(Fore.WHITE + Style.BRIGHT + "  ┌─────────────────────────────┐")
    print("  │  1. 📋 Show Tasks            │")
    print("  │  2. ➕ Add Task              │")
    print("  │  3. ✅ Complete Task          │")
    print("  │  4. 🗑️  Delete Task           │")
    print("  │  5. 😂 Nag Mode              │")
    print("  │  6. 💌 Love Note             │")
    print("  │  7. 🚪 Exit                  │")
    print("  └─────────────────────────────┘" + Style.RESET_ALL)

def show_tasks(tasks):
    """Display all tasks"""
    if not tasks:
        print(Fore.YELLOW + "\n  No tasks yet! Add some and get productive! ✨" + Style.RESET_ALL)
        return
    
    print(Fore.WHITE + Style.BRIGHT + "\n  ═══════ YOUR TASKS ═══════\n" + Style.RESET_ALL)
    
    for i, task in enumerate(tasks, 1):
        status = Fore.GREEN + "✅" if task["done"] else Fore.RED + "⬜"
        priority = PRIORITIES[task["priority"]]
        color = priority["color"]
        label = priority["label"]
        
        # Strike-through effect for completed tasks
        name = task["name"]
        if task["done"]:
            name = Fore.GREEN + f"~~{name}~~" + Style.RESET_ALL
        
        date_added = task.get("date", "")
        
        print(f"  {status} {Style.RESET_ALL}{Fore.WHITE}{i}. {color}{label} {Style.RESET_ALL}│ {name} {Fore.LIGHTBLACK_EX}({date_added}){Style.RESET_ALL}")
    
    show_progress_bar(tasks)

def add_task(tasks):
    """Add a new task"""
    print(Fore.CYAN + "\n  ── Add New Task ──" + Style.RESET_ALL)
    
    name = input(Fore.WHITE + "\n  📝 What needs to be done? → " + Style.RESET_ALL).strip()
    if not name:
        print(Fore.RED + "  Task can't be empty, silly! 😜" + Style.RESET_ALL)
        return
    
    print(Fore.WHITE + "\n  Priority level:" + Style.RESET_ALL)
    print("    1. 🔥 URGENT  (do it NOW!)")
    print("    2. ⭐ Important (do it soon)")
    print("    3. 🌙 Chill (whenever you feel like it)")
    
    priority = input(Fore.WHITE + "\n  Choose (1/2/3) → " + Style.RESET_ALL).strip()
    if priority not in ["1", "2", "3"]:
        priority = "2"  # Default to important
    
    task = {
        "name": name,
        "priority": priority,
        "done": False,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    
    tasks.append(task)
    save_tasks(tasks)
    
    print(Fore.GREEN + f"\n  ✅ Added: '{name}' — You got this, babe! 💪" + Style.RESET_ALL)

def complete_task(tasks):
    """Mark a task as complete"""
    pending = [(i, t) for i, t in enumerate(tasks) if not t["done"]]
    
    if not pending:
        print(Fore.GREEN + "\n  All tasks done! You're a LEGEND! 🏆👑" + Style.RESET_ALL)
        return
    
    show_tasks(tasks)
    
    try:
        num = int(input(Fore.WHITE + "\n  Which task did you finish? (number) → " + Style.RESET_ALL))
        if 1 <= num <= len(tasks):
            tasks[num - 1]["done"] = True
            save_tasks(tasks)
            
            # Random cute message!
            message = random.choice(completion_messages)
            print(Fore.GREEN + Style.BRIGHT + f"\n  {message}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "  That task doesn't exist! 🤔" + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "  Please enter a number! 😅" + Style.RESET_ALL)

def delete_task(tasks):
    """Delete a task"""
    if not tasks:
        print(Fore.YELLOW + "\n  Nothing to delete! The list is empty 🤷" + Style.RESET_ALL)
        return
    
    show_tasks(tasks)
    
    try:
        num = int(input(Fore.WHITE + "\n  Which task to delete? (number) → " + Style.RESET_ALL))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks(tasks)
            print(Fore.YELLOW + f"\n  🗑️ Deleted: '{removed['name']}' — Gone forever!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "  That task doesn't exist! 🤔" + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "  Please enter a number! 😅" + Style.RESET_ALL)

def nag_mode(tasks):
    """Funny reminders for unfinished tasks"""
    pending = [t for t in tasks if not t["done"]]
    
    if not pending:
        print(Fore.GREEN + "\n  Nothing to nag about! You're perfect! 💯" + Style.RESET_ALL)
        return
    
    print(Fore.MAGENTA + Style.BRIGHT + "\n  ══ 😂 NAG MODE ACTIVATED 😂 ══\n" + Style.RESET_ALL)
    
    for task in pending:
        nag = random.choice(nag_messages)
        print(Fore.MAGENTA + f"  📢 '{task['name']}'")
        print(Fore.LIGHTYELLOW_EX + f"     → {nag}\n" + Style.RESET_ALL)

def love_note():
    """Leave a secret love note"""
    notes = [
        "I just wanted to say... I love you! 💝",
        "You're the best thing that ever happened to me 🥺",
        "Hey handsome, don't forget to drink water! 💧",
        "I believe in you! You can do ANYTHING! 🚀",
        "Just thinking about you makes me smile 😊",
        "You + Me = ❤️ (that's the only math I like)",
        "I'm so lucky to have you 🍀",
        "You make my heart go 💓💓💓",
        "Plot twist: You're amazing and everyone knows it 👑",
        "Sending you a virtual hug right now 🤗",
    ]
    
    print(Fore.MAGENTA + Style.BRIGHT + "\n  ╔═══════════════════════════════╗")
    print(f"  ║  💌 {random.choice(notes)}")
    print("  ╚═══════════════════════════════╝" + Style.RESET_ALL)

# ============== MAIN APP ==============

def main():
    """Run the app"""
    tasks = load_tasks()
    
    clear_screen()
    show_header()
    print(Fore.MAGENTA + f"  {random.choice(welcome_messages)}\n" + Style.RESET_ALL)
    
    while True:
        show_menu()
        
        choice = input(Fore.WHITE + Style.BRIGHT + "\n  What do you want to do? → " + Style.RESET_ALL).strip()
        
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            nag_mode(tasks)
        elif choice == "6":
            love_note()
        elif choice == "7":
            print(Fore.MAGENTA + Style.BRIGHT + "\n  Bye bye! Don't forget you're amazing! 💝👋\n" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "  Hmm, that's not an option! Try 1-7 😊" + Style.RESET_ALL)
        
        input(Fore.LIGHTBLACK_EX + "\n  Press Enter to continue..." + Style.RESET_ALL)
        clear_screen()
        show_header()

# Run the app!
if __name__ == "__main__":
    main()