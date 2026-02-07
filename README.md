# Screen Capturer

Small tool to grab a piece of your screen.

Click "Capture", drag a rectangle anywhere (works with multiple monitors),  
let go → the picture goes to clipboard + coords too + tiny preview shows up.

You can then save it or copy the image/coords again.

Looks a bit like the windows snipping tool but way simpler and dark.

# What you need

- Python 3 (probably 3.8 or newer is safest)
- PyQt5

Just do:

pip install PyQt5

# How to start it

python main.py

(or whatever you named the file with the if __name__ == "__main__" part)

That's it.

Click Capture → drag → done.

Buttons appear when you finish selecting:
- Copy Image
- Copy Coords
- Save

Coords look like (100, 200, 800, 600)

# Files

main.py                  ← starts everything
screen_region_selector.py ← the little window with buttons
capture.py               ← the fullscreen thing where you drag

Put them in one folder and run main.py

Have fun.
If it crashes on Linux/macOS let me know what error you get.
