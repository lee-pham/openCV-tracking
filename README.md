# openCV-tracking
My attempt at the world of computer vision. More specifically, openCV with the Rasperry Pi 2 Model B and camera module.
Written in Python.

This is an extremely basic foray into object tracking with [openCV](http://opencv.org/). By converting an image to the *H*ue *S*aturation *V*alue color space, it is easier to track a uniformly colored object, as opposed to the typical *BGR** color space. (*In openCV's case, the image arrays are interpreted as  [Blue, Green, Red], *NOT* [Red, Green, Blue])

A range of acceptable HSV ranges are added in and your (uniformly) colored object of choice should be the only thing to appear.

Use the HSVPreview.py program to obtain your minimum and maximum values.

RectangularOverlay.py is the same as ObjectFilter.py except for an added rectangular overlay.

Much thanks to @abidrahmank and his [Open-CV-Python Tutorials](https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html) in which I was able to learn most of this. Also, thanks to @ladvien and his [How to Track your Robot with OpenCV](http://www.instructables.com/id/How-to-Track-your-Robot-with-OpenCV/?ALLSTEPS) guide.
