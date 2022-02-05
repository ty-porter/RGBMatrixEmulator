# RGBMatrixEmulator Samples

Samples in this directory have been adapted from [`rpi-rgb-led-matrix` Python samples](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python/samples).

## Installing Samples

Installation of `RGBMatrixEmulator` from PyPi does not include sample files. After installing the emulator according to the [README](../README.md#installation), you should clone this repository instead:

SSH:

```sh
git clone git@github.com:ty-porter/RGBMatrixEmulator.git
```

HTTPS:

```sh
git clone https://github.com/ty-porter/RGBMatrixEmulator.git
```

## Usage

Navigate to the `samples` directory:

```sh
cd samples
```

Run individual samples with valid `RGBMatrixEmulator` options. See the chart below for a description of each sample with additional required arguments.

## Samples

Below is a list of all samples included for `RGBMatrixEmulator`. Unless otherwise specified, the syntax for running the command is simply `python NAME_OF_SCRIPT`, plus any optional arguments you choose to use.

Sample images (`sample/images`) and fonts (`sample/fonts`) are included for use with the samples below. In normal use cases these are already included with the project you are emulating if installing the emulator into an existing script. If you're developing a script from scratch, you will need to provide your own.

| Name | Optional Arguments | Description |
| ---- | --------------- | ----------- |
| `graphics` |  | A simple graphics routine for drawing text, lines, and circles |
| `grayscale_block` | | A graphics routine for grayscale colors |
| `image-draw` | | Draws an image using `PIL` and slides it across the display
| `image-scroller` | `-i` / `--image` | Scrolls an image from a file. Defaults to `samples/images/runtext.ppm` unless optional arguments included |
| `image-viewer` | Required second argument (path to image) | Draws a static image from a file |
| `pulsing-brightness` | | Example of manipulating pixel brightness |
| `pulsing-colors` | | Example of manipulating pixel color |
| `rotating-block-generator` | | Draws a rotating multicolored block |
| `runtext` | `-t` / `--text` | Scrolls `HELLO WORLD` text unless optional arguments included |
| `samplebase` | | **DO NOT USE DIRECTLY**. Base class for driver setup, argument parsing, etc. |
| `simple-square` | | A simple graphics drawing routine |

## Other Projects

Examples of larger projects:

* [mlb-led-scoreboard-emulated](https://github.com/ty-porter/mlb-led-scoreboard-emulated)
* [nfl-led-scoreboard-emulated](https://github.com/ty-porter/nfl-led-scoreboard-emulated)