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
from pynput.keyboard import Key, KeyCode, Listener
from keysym_map import get_keysym_for_char
from send_keycode import send_keycode
from Xlib.xobject.drawable import Window

SHIFT_CHARS = set('~!@#$%^&*_+{}()|:"<>?')
LINE_SIZE = 44


class DarkAgesPresenter:
    def __init__(self, text_file: str, delay: float = 0.1, verbose: bool = False):
        self.text_file: Path = Path(text_file)
        self.delay: float = delay
        self.verbose: bool = verbose
        self.paused: bool = False
        self.running: bool = True
        self.display: Xlib.display.Display = Xlib.display.Display()
        self.target_window: Window | None = None
        self.shift_code: int = self.display.keysym_to_keycode(Xlib.XK.XK_Shift_L)
        self.enter_code: int = self.display.keysym_to_keycode(Xlib.XK.XK_KP_Enter)

        # Setup keyboard listener for alt pause
        self.listener: Listener = Listener(on_press=self._on_key_press)

    def _on_key_press(self, key: KeyCode | Key | None) -> None:
        """Handle f2 press for pause/unpause"""
        if key == Key.f2:
            self.paused = not self.paused
            status = "PAUSED" if self.paused else "RESUMED"
            print(f"\n[{status}] Press F2 to {'resume' if self.paused else 'pause'}")

    def find_dark_ages_window(self) -> Window | None:
        """Find first window with name 'Darkages'. Will not function properly if multiple such windows exist."""
        root: Window = self.display.screen().root  # pyright: ignore[reportAny]

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
                children: list[Window] = window.query_tree().children  # pyright: ignore[reportAny]
                for child in children:
                    result = search_windows(child)
                    if result:
                        return result
            except Exception:
                pass
            return None

        return search_windows(root)

    def send_text_to_window(self, text: str) -> bool:
        """Send text to the target window"""
        if not self.target_window:
            return False

        # Focus the window first
        self.target_window.set_input_focus(Xlib.X.RevertToParent, Xlib.X.CurrentTime)
        self.display.sync()

        character_count = 0
        # Send each character
        for char in text:
            if self.verbose:
                print("Sending:", repr(char))
            if not self.running:
                break

            # Wait while paused
            while self.paused and self.running:
                time.sleep(0.25)

            if not self.running:
                break

            # Convert character to keysym and send
            # convert to lowercase for keysym lookup
            shift = False
            if char.isupper() or char in SHIFT_CHARS:
                if self.verbose:
                    print(" (with SHIFT)")
                shift = True

            # Handle special characters
            keysym = get_keysym_for_char(char)
            if keysym is None:
                if self.verbose:
                    print(f"Warning: Unsupported character '{char}'")
                keysym = Xlib.XK.string_to_keysym(char)
                if keysym == 0:
                    if self.verbose:
                        print(f"Error: Unsupported character '{char}', skipping")
                    continue  # Skip unsupported characters
            if keysym == Xlib.XK.XK_Return:
                # break on newlines
                if character_count > 0:
                    if self.verbose:
                        print(" (ENTER)")
                    self.send_keycode(self.enter_code)
                # long pause for multiple newlines
                else:
                    if self.verbose:
                        print(" (LONG PAUSE)")
                    time.sleep(self.delay * LINE_SIZE / 2)
                character_count = 0
                continue

            keycode = self.display.keysym_to_keycode(keysym)
            if self.verbose:
                print(f" (keycode {keycode})")
            # 0 is the keysym_to_keycode return value for unsupported characters
            # start new Dark Ages speech
            if character_count == 0:
                if self.verbose:
                    print(" (ENTER)")
                self.send_keycode(self.enter_code)
            # send speech line and start a new one
            elif character_count >= LINE_SIZE and char == " ":
                if self.verbose:
                    print(" (ENTER)")
                self.send_keycode(self.enter_code)
                character_count = 0
                continue

            # Send key press and release, with shift if needed
            if self.verbose:
                print(f" (sending keycode {keycode} with shift={shift})")
            self.send_keycode(keycode, shift)
            character_count += 1
        return True

    def send_keycode(self, keycode: int, is_upper: bool = False) -> None:
        send_keycode(
            self.target_window,
            self.display,
            keycode,
            self.shift_code,
            self.delay,
            is_upper,
        )

    def run(self) -> bool:
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
            print("Starting in 3 seconds...")
            print("Press CTRL+C within the terminal window to quit.")
            print("Or press F2 within Dark Ages to pause.")

            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)

            print("Starting the reading...")

            # Send text
            success = self.send_text_to_window(text_content)

            if success:
                print("\nReading completed!")
            else:
                print("\nReading interrupted or failed")

        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.running = False
            self.listener.stop()

        return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send keystrokes to Dark Ages window from text file"
    )
    _ = parser.add_argument(
        "text_file", help="Path to text file containing keystrokes to send"
    )
    _ = parser.add_argument(
        "-d",
        "--delay",
        type=int,
        default=5,
        help="Delay between keystrokes 1-10 (default: 5)",
    )

    _ = parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output (default: False)",
    )

    args = parser.parse_args()

    # Delay mapping: index 0 is unused, 1-10 are valid
    delay_options = [0, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.175, 0.185, 0.2]
    delay = delay_options[5]  # default 0.14 seconds
    if not isinstance(args.delay, int):  # pyright: ignore[reportAny]
        print(
            f"Invalid delay value, using default of {delay} seconds between keystrokes"
        )
    if 1 <= args.delay <= 10:
        delay = delay_options[args.delay]
    else:
        print(
            f"Invalid delay value, using default of {delay} seconds between keystrokes"
        )
    presenter = DarkAgesPresenter(args.text_file, delay, args.verbose)  # pyright: ignore[reportAny]
    _ = presenter.run()


if __name__ == "__main__":
    main()
