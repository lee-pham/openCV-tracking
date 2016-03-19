# openCV-tracking
My attempt at the world of computer vision. More specifically, openCV with the Rasperry Pi 2 Model B and camera module.
Written in Python.

*Currently in progress: Auto upper and lower bound HSV selection*
>In the `/clickdrag/` folder, I have uploaded two files that involve openCV's `HighGUI` modules. It involves creating a rectangular overlay by clicking and dragging the mouse around the Region of Interest (ROI). 

>For the static edition, an initial copy of the image is made, so when a new mouse callback occurs, the image will be reset to the original, and a new rectangle will be drawn using the initial point, and the current mouse position. Having the copy, and recalling the copy prevents rectangles being overwritten on an image with rectanles already on it.

>For videos, a different approach had to be taken as a new image is being constantly written at all times. The copy method was foregoed and drawing the rectangles had to be moved to the main video loop. Essentially, a rectangle is constantly being drawn at all times, as opposed to a rectangle being drawn once, with the same image being constantly displayed.

>I've spent a great deal of time figuring out how to best draw rectangles (without a following cascade) for static and video--I hope this helps!





This is an extremely basic foray into object tracking with [openCV](http://opencv.org/). By converting an image to the **H**ue **S**aturation **V**alue color space, it is easier to track a uniformly colored object, as opposed to the typical **BGR** color space. (In openCV's case, the image arrays are interpreted as  [Blue, Green, Red], **_NOT_** [Red, Green, Blue])

A range of acceptable HSV ranges are added in and your (uniformly) colored object of choice should be the only thing to appear.

Use the HSVPreview.py program to obtain your minimum and maximum values.

RectangularOverlay.py is the same as ObjectFilter.py except for an added rectangular overlay.

Much thanks to @abidrahmank and his [Open-CV-Python Tutorials](https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html) in which I was able to learn most of this. Also, thanks to @ladvien and his [How to Track your Robot with OpenCV](http://www.instructables.com/id/How-to-Track-your-Robot-with-OpenCV/?ALLSTEPS) guide.
