#!/usr/bin/env python3
"""
Dark Ages Presenter - Automated keystroke sender for Dark Ages windows
"""

import argparse
import time
from pathlib import Path

import Xlib
import Xlib.display
import Xlib.X
from Xlib.protocol import event
from Xlib.xobject.drawable import Window
from pynput.keyboard import Key, Listener


class DarkAgesPresenter:
    def __init__(self, text_file: str, delay: float = 0.1):
        self.text_file: Path = Path(text_file)
        self.delay: float = delay
        self.paused: bool = False
        self.running: bool = True
        self.display: Xlib.display.Display = Xlib.display.Display()
        self.target_window: Window | None = None

        # Setup keyboard listener for spacebar pause
        self.listener: Listener = Listener(on_press=self._on_key_press)

    def find_dark_ages_window(self):
        """Find window with name 'Darkages'"""
        root = self.display.screen().root

        def check_window(window: Window) -> Window | None:
            try:
                wm_name = window.get_wm_name()
                if wm_name and "Darkages" in str(wm_name):
                    return window
            except Exception:
                pass
            return None

        # Check all windows recursively
        def search_windows(window: Window) -> Window | None:
            result = check_window(window)
            if result:
                return result

            try:
                children = window.query_tree().children
                for child in children:
                    result = search_windows(child)
                    if result:
                        return result
            except Exception:
                pass
            return None

        return search_windows(root)

    def _on_key_press(self, key):
        """Handle spacebar press for pause/unpause"""
        if key == Key.space:
            self.paused = not self.paused
            status = "PAUSED" if self.paused else "RESUMED"
            print(
                f"\n[{status}] Press spacebar to {'resume' if self.paused else 'pause'}"
            )

    def send_text_to_window(self, text: str):
        """Send text to the target window"""
        if not self.target_window:
            return False

        # Focus the window first
        self.target_window.set_input_focus(Xlib.X.RevertToParent, Xlib.X.CurrentTime)
        self.display.sync()

        # Send each character
        for char in text:
            if not self.running:
                break

            # Wait while paused
            while self.paused and self.running:
                time.sleep(0.1)

            if not self.running:
                break

            # Convert character to keysym and send
            keysym = Xlib.XK.string_to_keysym(char)
            if keysym == 0:  # Handle special characters
                if char == "\n":
                    keysym = Xlib.XK.XK_Return
                elif char == "\t":
                    keysym = Xlib.XK.XK_Tab
                elif char == " ":
                    keysym = Xlib.XK.XK_space
                else:
                    continue  # Skip unsupported characters

            keycode = self.display.keysym_to_keycode(keysym)
            if keycode != 0:
                # Send key press and release
                self.target_window.send_event(
                    event.KeyPress(
                        time=int(time.time()),
                        root=self.display.screen().root,
                        window=self.target_window,
                        same_screen=1,
                        child=Xlib.X.NONE,
                        root_x=0,
                        root_y=0,
                        event_x=0,
                        event_y=0,
                        state=0,
                        detail=keycode,
                    )
                )

                self.target_window.send_event(
                    event.KeyRelease(
                        time=int(time.time()),
                        root=self.display.screen().root,
                        window=self.target_window,
                        same_screen=1,
                        child=Xlib.X.NONE,
                        root_x=0,
                        root_y=0,
                        event_x=0,
                        event_y=0,
                        state=0,
                        detail=keycode,
                    )
                )

                self.display.sync()
                time.sleep(self.delay)

        return True

    def run(self):
        """Main execution loop"""
        # Start keyboard listener
        self.listener.start()

        try:
            # Find target window
            print("Searching for Dark Ages window...")
            self.target_window = self.find_dark_ages_window()

            if not self.target_window:
                print("Error: No window found with 'dark ages' in class name")
                return False

            print(f"Found target window: {self.target_window.get_wm_name()}")

            # Read text file
            if not self.text_file.exists():
                print(f"Error: File '{self.text_file}' not found")
                return False

            with open(self.text_file, "r", encoding="utf-8") as f:
                text_content = f.read()

            print(f"Loaded {len(text_content)} characters from {self.text_file}")
            print("Starting in 3 seconds... Press spacebar to pause/resume")

            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)

            print("GO!")

            # Send text
            success = self.send_text_to_window(text_content)

            if success:
                print("\nText sending completed!")
            else:
                print("\nText sending interrupted or failed")

        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.running = False
            self.listener.stop()

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Send keystrokes to Dark Ages window from text file"
    )
    parser.add_argument(
        "text_file", help="Path to text file containing keystrokes to send"
    )
    parser.add_argument(
        "--delay",
        "-d",
        type=float,
        default=0.1,
        help="Delay between keystrokes in seconds (default: 0.1)",
    )

    args = parser.parse_args()

    presenter = DarkAgesPresenter(args.text_file, args.delay)
    presenter.run()


if __name__ == "__main__":
    main()
