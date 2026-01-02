# Pi5 Adapter

> [!NOTE]  
> This adapter is currently experimental. Please report issues to https://github.com/ty-porter/RGBMatrixEmulator/issues

This adapter enables the RGBMatrixEmulator to drive RGB led matrices connected to a Raspberry Pi 5 using the `adafruit-circuitpython-piomatter` library. It bridges the emulator's frame generation with the PIO-based hardware driving capabilities of the Pi 5.

## Configuration

The adapter is configured via the `pi5` section in your `emulator_config.json`.

### Options

| Option | Type | Description |
| :--- | :--- | :--- |
| `pinout` | String | The hardware pinout definition. Matches attributes in `piomatter.Pinout` (e.g., `"Active3","AdafruitMatrixHat","AdafruitMatrixBonnet"`). |
| `n_addr_lines` | Integer | Number of address lines for the display. Typically `4` for 32-pixel height panels, or `5` for 64-pixel height panels. |
| `led_rgb_sequence` | String | Color sequence of the LEDs (e.g., `"RGB"`, `"BGR"`, `"RBG"`). |
| `rotation` | String | Display rotation. Matches attributes in `piomatter.Orientation` (e.g., `"Normal"`, `"R180"`, `"CW"`, `"CCW"`). Does not work with `"Active3"` pinouts. |
| `n_lanes` | Integer | Number of parallel matrix chains (lanes). Only works with Active3 boards.  Must be 2 or more. |
| `n_planes` | Integer | Colour Bit depth/number of planes. Maximum of 10, minimum of 1|
| `n_temporal_planes` | Integer | Number of temporal planes for dithering/brightness control. Possible values are 0, 2 or 4 and can't be greater than the value of n_planes. |

### Example Configuration

```json
"pi5": {
  "pinout": "AdafruitMatrixBonnet",
  "n_addr_lines": 4,
  "led_rgb_sequence": "RGB",
  "rotation": "Normal",
  "n_lanes": 2,
  "n_planes": 6,
  "n_temporal_planes": 0
}
```

## Setup & Non-Root Access

By default, accessing the PIO subsystem on the Raspberry Pi 5 requires root privileges (`sudo`). To run the adapter as a standard user, you must configure a `udev` rule.

### configuring `udev` Rules

1.  Create or edit the file `/etc/udev/rules.d/99-com.rules`:

    ```bash
    sudo nano /etc/udev/rules.d/99-com.rules
    ```

2.  Add the following line to the file:

    ```text
    SUBSYSTEM=="*-pio", GROUP="gpio", MODE="0660"
    ```

3.  Save the file (Ctrl+S, then Ctrl+X) and reboot your Raspberry Pi:

    ```bash
    sudo reboot
    ```

For more details, refer to the [Adafruit Raspberry Pi 5 Setup Guide](https://learn.adafruit.com/rgb-matrix-panels-with-raspberry-pi-5/raspberry-pi-5-setup#add-pio-subsystem-rule-configuration-3191958).
