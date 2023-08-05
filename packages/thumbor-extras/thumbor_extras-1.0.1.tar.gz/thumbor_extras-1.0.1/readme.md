# thumbor_extras

Some useful extensions to [thumbor](https://thumbor.readthedocs.io/en/latest/index.html) - extra filters and detectors.

```
pip install thumbor_extras
```

## Detectors

Add these detectors to your `thumbor.conf`:

```
DETECTORS = [
    'thumbor_extras.detectors.dnn_face_detector',
    'thumbor_extras.detectors.dnn_object_detector'
]
```

### dnn_face_detector

An improved face detector that uses a deep neural network. More specifically, it uses the [SSD object detection model](https://arxiv.org/abs/1512.02325), trained specifically on faces. According to [the OpenCV repo](https://github.com/opencv/opencv/blob/master/samples/dnn/face_detector/how_to_train_face_detector.txt), it was trained with "some huge and available online dataset." :/

For more information on how the normal thumbor face detector compares to this one in both accuracy and efficiency, see [this comparison script](https://github.com/imaus10/compare_face_detection).

### dnn_object_detector

The full SSD object detection model, trained on the [COCO dataset](http://cocodataset.org). It was built as a [MobileNet](https://arxiv.org/abs/1704.04861), a class of efficient, light weight deep neural network models meant to work well in mobile and embedded applications.

## Filters

Add these filters to your available filters in `thumbor.conf`:

```
FILTERS = [
    ...other filters,
    'thumbor_extras.filters.draw_center_of_mass',
    'thumbor_extras.filters.draw_focal_points'
]
```

### draw_center_of_mass

Draws a circle at the calculated center of mass, according to the focal points.

Usage: `draw_center_of_mass([r, g, b])`

Examples:
- `draw_center_of_mass()`: draws a circle with default red color.
- `draw_center_of_mass(0,0,255)`: draws a blue circle.

### draw_focal_points

Draws a box around the focal points, for displaying the results of the detectors on a given image. Takes optional arguments for box color and line width.

Usage: `draw_focal_points([line_width, show_heatmap, show_labels, show_rainbow, r, g, b])`

Arguments:

- `line_width`: the width of the box lines
- `show_heatmap`: make the box more opaque for higher-confidence detections, more transparent for less confident detections
- `show_labels`: print the class label at the top of the box
- `show_rainbow`: use a different color for each focal point box; pass false to provide a single color RGB value for all boxes
- `r`: R component of RGB color of box, default 0
- `g`: G component of RGB color of box, default 255
- `b`: B component of RGB color of box, default 0

Examples:
- `draw_focal_points()`: draws boxes with defaults (green color and 3 pixel line width).
- `draw_focal_points(5,false,false,false,255,0,0)`: draws solid red boxes with 5 pixel line width, and no class labels.

## TODO

- Choose thresholds empirically

## Development

Because I will definitely forget. Python development can be a pain.

```
# -- ENV --
# use python 2 - thumbor doesn't support 3 yet.
virtualenv thumbor_env --python=/path/to/python2
source thumbor_env/bin/activate

# -- DEVELOP --
pip install -e .

# -- TEST --
# i don't know why setup.py can't install pytest...but it fails without manual install.
# it could be a python2 / mac thing.
pip install pytest
python setup.py test

# -- DISTRIBUTE --
python setup.py sdist
# make a wheel from the source tarball (to use manifest correctly)
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
pip install twine
# make sure pip URLs are configured per https://truveris.github.io/articles/configuring-pypirc/
python -m twine upload --repository pypi dist/*
```
