# `raw` Display Adapter

The `raw` adapter gives fine-grained control over the pixel buffer while RGBME is running. By default, it does not display any pixels and simply caches the prior buffers for use later.

This adapter powers the [integration tests](/test) for this project. For more details how this was accomplished, see the accompanying [blog post](https://blog.ty-porter.dev/development/emulation/2025/02/04/how-to-test-your-emulator.html).

## Configuring the `raw` Adapter

For configuration of the display adapter, check the main [README's configuration section](../../../README.md#configuration-options).

Your code needs special handling to take advantage of the features of this adapter.

```python
# Assuming you have a fully formed RGBMatrix object, access the adapter through a Canvas.

adapter = matrix.canvas.display_adapter
```

## Halting Execution

You can halt execution of the adapter after X frames as follows:

```python
adapter.halt_after = 10
adapter.halt_fn = lambda: raise "HALTED"
```

This will halt execution after 10 frames by raising a `RuntimeError:  "HALTED"`.

## Dumping a Screenshot

```python
adapter._dump_screenshot("path/to/screenshot.png")
```

## Accessing the Pixel Buffer

By default, the adapter stores up to 128 frames, overwriting the oldest frame once the cap is reached.

```python
# Last frame
adapter._last_frame()

# All frames
adapter.frames
```

The frame buffer is a 3D numpy array of size matrix height by matrix width by 3-tuple RGB. Using this data you can draw pixels however you please.
