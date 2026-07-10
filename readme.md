# Desktop POP-UP Break Reminder

A lightweight, animated desktop break reminder built with Python. At customizable intervals, an animated character seamlessly slides onto your screen with a fully transparent background to remind you to take a well-deserved break, plays its animation, and slides away.
Unlike standard rectangular notifications, this app uses real-time color keying to remove the video background completely, making the character look like it is walking directly on top of your desktop wallpaper.

---

## 🚀 Features

* **Zero-Border Transparency:** No ugly windows or background boxes—just the character overlaying your screen.
* **Fluid Animations:** Smoothly slides in from the right edge of the screen and slides back out when finished.
* **Customizable Timer:** Easily set your preferred work interval in minutes.
* **Always on Top:** The reminder stays visible over open browser tabs or code editors so you don't miss it.
* **Console Countdown:** Keeps track of your remaining focus time right in your terminal.

---

## 🛠️ How It Works

The project shifts away from heavy external media players to use a native desktop GUI approach:
1. **System Timer:** A background loop tracks your focus interval.
2. **Native GUI Overlay:** When the timer hits zero, a borderless `tkinter` window is spawned and positioned off-screen.
3. **Real-Time Chroma Keying:** Using `OpenCV` (`cv2`), the script decodes the video frame-by-frame, identifies the green-screen background values, and dynamically swaps them with Windows' native transparency layer key (`#000100`).
4. **Hardware Motion:** The window coordinates are systematically incremented to create a clean "sliding" entrance and exit effect.

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
### 3. Add Your Video Asset
Ensure your green-screen animation file (e.g., Animation-greenbg.mp4) is saved inside the exact same directory as your Python script.

## 🏃‍♂️ Usage
Simply run the script using your terminal:
```bash
python break_reminder.py
```
The script will immediately trigger a test animation (if configured to do so).
A countdown timer will display in the console showing the exact time remaining until your next break.
To stop the application at any time, press Ctrl + C in your terminal window.
