# Desktop POP-UP Break Reminder

A lightweight, animated desktop break reminder built with Python that implements a custom Pomodoro productivity loop. At customizable intervals, animated characters seamlessly slide onto your screen with a fully transparent background to manage your work sessions and rest periods.
Unlike standard rectangular notifications, this app uses real-time color keying to remove the video backgrounds completely, making the characters look like they are walking directly on top of your desktop wallpaper.

---

## 🚀 Features

* **Dynamic Time Setup:** Asks you for your custom focus and rest intervals in the terminal every time you start the app (with easy defaults).
* **Pomodoro Loop System:** Automatically alternates between dedicated Focus Blocks and Rest Blocks.
* **Dual-Video Support:** Plays a designated "Take a Break" animation when focus time ends, and a "Break Over" animation when it's time to return to work.
* **Zero-Border Transparency:** No ugly windows or background boxes—just the character overlaying your screen.
* **Fluid Animations:** Smoothly slides in from the right edge of the screen and slides back out when finished.
* **Always on Top:** The reminders stay visible over open browser tabs or code editors so you don't miss them.
* **Console Countdown:** Keeps track of your remaining focus or rest time right in your terminal.

---

## 🛠️ How It Works

The project shifts away from heavy external media players to use a native desktop GUI approach:
1. **Interactive Setup:** Prompts the user via terminal for focus and rest durations, falling back to safe defaults if left empty.
2. **System Timer Loop:** A background loop tracks the focus interval, finishes, triggers the break sequence, tracks the rest interval, and restarts the cycle.
3. **Native GUI Overlay:** When a timer hits zero, a borderless `tkinter` window is spawned and positioned off-screen.
4. **Real-Time Chroma Keying:** Using `OpenCV` (`cv2`), the script decodes the designated video frame-by-frame, identifies the green-screen background values, and dynamically swaps them with Windows' native transparency layer key (`#000100`).
5. **Hardware Motion:** The window coordinates are systematically incremented to create a clean "sliding" entrance and exit effect.

---

## 📦 Prerequisites & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/transparent-break-reminder.git](https://github.com/YOUR_USERNAME/transparent-break-reminder.git)
cd transparent-break-reminder
```
### 2. Install Dependencies
Make sure you have Python installed, then install the required image processing and computer vision libraries:
```bash
pip install opencv-python pillow
```
### 3. Add Your Video Assets
Ensure both of your green-screen animation files are saved inside the exact same directory as your Python script:

- Animation-greenbg.mp4 (Triggered at the start of a break)
- BreakOver-greenbg.mp4 (Triggered when the break ends)

## 🏃‍♂️ Usage
Simply run the script using your terminal:
```bash
python break_reminder.py
```
1. Enter Your Time: The terminal will prompt you to set your timing preferences. Type a number and hit Enter, or simply hit Enter without typing to use your defaults.

2. Focus Mode: The script will enter [FOCUS MODE] and kick off your work block countdown.

3. Automated Reminders: Once focus ends, your character slides out to announce break time. The terminal shifts automatically to [BREAK MODE]. Once the rest timer finishes, your break-over animation will trigger, looping the cycle completely.

To stop the application at any time, press Ctrl + C in your terminal window.
