from graphics import *
import time

def timer():
    win = GraphWin("Timer", 200, 200)
    win.setBackground("white")
    start_time = time.time()
    last_update_time = start_time
    last_seconds = 60
    seconds = last_seconds

    timer_text = Text(Point(win.getWidth() / 2, win.getHeight() / 2), "60")
    timer_text.setSize(36)
    timer_text.draw(win)

    while True:
        current_time = time.time()
        if current_time - last_update_time >= 1:  # Only update once per second
            elapsed_time = current_time - start_time
            seconds = 60 - int(elapsed_time)

            # Check if a second has passed since last update
            if seconds != last_seconds:
                timer_text.setText(f'{seconds:02d}')
                last_seconds = seconds

            last_update_time = current_time  # Record the time of this update

        if win.checkMouse() or seconds == 0:  # exit if the window is clicked
            break

    win.close()

if __name__ == "__main__":
    timer()
