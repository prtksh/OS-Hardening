import os
import curses
import subprocess

def execute_command(command):
    os.system(command + " | tee /tmp/curses_output")
    os.system("clear")
    with open("/tmp/curses_output", "r") as file:
        return file.read()

def show_firewall_status(stdscr):
    stdscr.clear()
    result = subprocess.getoutput("ufw status")
    stdscr.addstr(2, 2, "Firewall Status:")
    stdscr.addstr(4, 2, result)
    stdscr.addstr(10, 2, "Press any key to go back.")
    stdscr.refresh()
    stdscr.getch()
        
def show_submenu(stdscr, menu_title, menu_options, commands):
    selected = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(1, w // 2 - len(menu_title) // 2, menu_title, curses.A_BOLD)
        
        for idx, item in enumerate(menu_options):
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(4 + idx, 2, item)
            if idx == selected:
                stdscr.attroff(curses.A_REVERSE)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(menu_options) - 1:
            selected += 1
        elif key == 10:  # Enter key
            if selected == len(menu_options) - 1:  # Exit submenu
                break
            else:
                stdscr.clear()
                result = execute_command(commands[selected])
                stdscr.addstr(1, 2, "Command Output:")
                stdscr.addstr(2, 2, result)
                stdscr.addstr(h - 2, 2, "Press any key to return to menu...")
                stdscr.refresh()
                stdscr.getch()



def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    main_menu = ["User Management", "Security Settings", "Check Firewall", "Exit"]
   
    firewall_options = ["Firewall status"]
    firewall_commands = ["ufw status"]

    user_management_options = [
        "Check Current User Privileges",
        "Create a New User",
        "Add User to a Group",
        "Remove User from sudo",
        "Back to Main Menu"
    ]
    user_management_commands = [
        "id $USER",
        "sudo adduser newuser",
        "sudo usermod -aG developers newuser",
        "sudo deluser newuser sudo"
    ]

    security_options = [
        "Restrict su Command",
        "Set Home Directory Permissions",
        "Disable Guest Account",
        "Disable Root Login via SSH",
        "Back to Main Menu"
    ]
    security_commands = [
        "sudo chmod 750 /bin/su",
        "chmod 700 /home/$USER",
        "echo -e '[SeatDefaults]\nallow-guest=false' | sudo tee -a /etc/lightdm/lightdm.conf && sudo systemctl restart lightdm",
        "sudo sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && sudo systemctl restart sshd"
    ]

    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(10, 5, "🛡 OS Hardening Tool 🛡")

        for idx, item in enumerate(main_menu):
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(4 + idx, 2, item)
            if idx == selected:
                stdscr.attroff(curses.A_REVERSE)

        key = stdscr.getch()
        
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(main_menu) - 1:
            selected += 1
        elif key == ord("\n"):
            if selected == 0:
                show_submenu(stdscr, "User Management", user_management_options, user_management_commands)
            elif selected == 1:
                show_submenu(stdscr, "Security Settings", security_options, security_commands)
            elif selected == 2:
                show_firewall_status(stdscr)
            elif selected == 3:
                break

curses.wrapper(main)

