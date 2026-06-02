# boot.py — runs before code.py and before REPL attaches to any display
import displayio

# Release any automatically detected displays
displayio.release_displays()


