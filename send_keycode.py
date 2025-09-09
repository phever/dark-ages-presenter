import time
import Xlib
from Xlib.display import Display
from Xlib.protocol import event
from Xlib.xobject.drawable import Window


def send_keycode(
    target_window: Window | None,
    display: Display,
    keycode: int,
    shift_code: int,
    delay: float,
    is_upper: bool = False,
):
    if not target_window:
        print(f"ERROR: Target Window not found... ERROR SENDING KEYCODE {keycode}")
        return

    if is_upper:
        target_window.send_event(
            event.KeyPress(
                time=int(time.time()),
                root=display.screen().root,
                window=target_window,
                same_screen=1,
                child=Xlib.X.NONE,
                root_x=0,
                root_y=0,
                event_x=0,
                event_y=0,
                state=0,
                detail=shift_code,
            )
        )

    target_window.send_event(
        event.KeyPress(
            time=int(time.time()),
            root=display.screen().root,
            window=target_window,
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

    target_window.send_event(
        event.KeyRelease(
            time=int(time.time()),
            root=display.screen().root,
            window=target_window,
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

    if is_upper:
        target_window.send_event(
            event.KeyRelease(
                time=int(time.time()),
                root=display.screen().root,
                window=target_window,
                same_screen=1,
                child=Xlib.X.NONE,
                root_x=0,
                root_y=0,
                event_x=0,
                event_y=0,
                state=0,
                detail=shift_code,
            )
        )

    display.sync()
    time.sleep(delay)
