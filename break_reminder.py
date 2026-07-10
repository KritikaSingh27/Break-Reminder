import os
import sys
import time
from datetime import datetime, timedelta

import cv2
from PIL import Image, ImageTk
import tkinter as tk


os.environ["SDL_RENDER_DRIVER"] = "software"
 
VIDEO_BREAK_START = "Animation-greenbg.mp4"
VIDEO_BREAK_OVER = "BreakOver-greenbg.mp4"

WORK_INTERVAL_MINUTES = 40 
BREAK_INTERVAL_MINUTES = 10

POPUP_WIDTH = 220
POPUP_HEIGHT = 391
MARGIN_FROM_EDGE = 20
SLIDE_STEP_PX = 20
SLIDE_DELAY_S = 0.01
WINDOW_TITLE = "BreakPopupReminder"
PLAY_IMMEDIATELY_ON_START = False

def play_popup(video_path):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Break time! Sliding in reminder...")

    # Open video file using OpenCV
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("[ERROR] Could not open video file.")
        return

    # Set up Tkinter overlay window
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.overrideredirect(True)  # Makes it borderless
    root.attributes("-topmost", True)  # Always on top
    
    # CRITICAL: Define a unique color to match and erase completely
    TRANSPARENT_COLOR = "#000100" 
    root.config(bg=TRANSPARENT_COLOR)
    root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)

    # Calculate positioning
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    y = (screen_h - POPUP_HEIGHT) // 2
    off_screen_x = screen_w + 10
    target_x = screen_w - POPUP_WIDTH - MARGIN_FROM_EDGE

    # Create image rendering frame
    label = tk.Label(root, bg=TRANSPARENT_COLOR, bd=0)
    label.pack()

    # Position initially off-screen, then slide in
    root.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{off_screen_x}+{y}")
    root.update()

    def slide_window(start, end):
        step = SLIDE_STEP_PX if end > start else -SLIDE_STEP_PX
        for current_x in range(start, end, step):
            root.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{current_x}+{y}")
            root.update()
            time.sleep(SLIDE_DELAY_S)
        root.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{end}+{y}")
        root.update()

    slide_window(off_screen_x, target_x)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    delay = max(1, int(1000 / fps) - 15)

    def update_frame():
        ret, frame = cap.read()
        if not ret:
            slide_window(target_x, off_screen_x)
            cap.release()
            root.destroy()
            return

        frame = cv2.resize(frame, (POPUP_WIDTH, POPUP_HEIGHT))
        
        # Convert video color formatting to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert any pixel that looks green into the transparency layer key color
        r, g, b = rgb_frame[:,:,0], rgb_frame[:,:,1], rgb_frame[:,:,2]
        green_pixels = (g > 100) & (g > r * 1.2) & (g > b * 1.2)
        rgb_frame[green_pixels] = [0, 1, 0] # Match the #000100 window color hex exactly

        # Render image frame in Tkinter window
        img = Image.fromarray(rgb_frame)
        img_tk = ImageTk.PhotoImage(image=img)
        label.config(image=img_tk)
        label.image = img_tk

        root.after(delay, update_frame)

    root.after(0, update_frame)
    root.mainloop()
 
def countdown(minutes):
    total_seconds = int(minutes * 60)
    next_time = datetime.now() + timedelta(seconds=total_seconds)
    print(f"Next break reminder at {next_time.strftime('%H:%M:%S')} "
          f"(in {minutes} minutes). Press Ctrl+C to stop.\n")
    while total_seconds > 0:
        mins, secs = divmod(total_seconds, 60)
        print(f"\r  Time until next break: {mins:02d}:{secs:02d}   ", end="", flush=True)
        time.sleep(1)
        total_seconds -= 1
    print()
 
 
def main():
    global WORK_INTERVAL_MINUTES, BREAK_INTERVAL_MINUTES
    script_dir = os.path.dirname(os.path.abspath(__file__))
    break_start_path = os.path.join(script_dir, VIDEO_BREAK_START)
    break_over_path = os.path.join(script_dir, VIDEO_BREAK_OVER)
    
    for path in (break_start_path, break_over_path):
        if not os.path.isfile(path):
            print(f"\n[ERROR] Missing video file at:\n  {path}")
            sys.exit(1)

    print("=" * 50)
    print(" Setup Your Custom Pomodoro Timer")
    print("=" * 50)
    try:
        user_work = input(f"Enter work duration in minutes [Default 40]: ").strip()
        if user_work.isdigit():
            WORK_INTERVAL_MINUTES = int(user_work)
            
        user_break = input(f"Enter break duration in minutes [Default 10]: ").strip()
        if user_break.isdigit():
            BREAK_INTERVAL_MINUTES = int(user_break)
    except (KeyboardInterrupt, SystemExit):
        print("\nSetup cancelled. Exiting.")
        sys.exit(0)

    print("=" * 50)
    print(" Pomodoro Break Loop Is Active!")
    print(f" Work Duration: {WORK_INTERVAL_MINUTES} minutes")
    print(f" Break Duration: {BREAK_INTERVAL_MINUTES} minutes")
    print("=" * 50)
 
    try:
        while True:
            # 1. Focus block countdown
            print(f"\n--- [FOCUS MODE] Starting {WORK_INTERVAL_MINUTES} mins of work ---")
            countdown(WORK_INTERVAL_MINUTES)
            
            # 2. Work timer ends -> Trigger "Take a Break" animation
            play_popup(break_start_path)
            
            # 3. Rest block countdown
            print(f"\n--- [BREAK MODE] Enjoy your {BREAK_INTERVAL_MINUTES} mins rest ---")
            countdown(BREAK_INTERVAL_MINUTES)
            
            # 4. Break timer ends -> Trigger "Break Over" animation
            play_popup(break_over_path)
 
    except KeyboardInterrupt:
        print("\n\nBreak Popup Reminder stopped. Bye!")
        sys.exit(0)
 
 
if __name__ == "__main__":
    main()
 