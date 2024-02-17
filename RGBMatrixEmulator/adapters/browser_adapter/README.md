# `browser` Display Adapter

The `browser` adapter operates differently than other `RGBMatrixEmulator` display adapters. Under the hood, the adapter is a full webserver and WebSocket wrapper and includes its own JS client that can render an emulated image from a Python script within the browser.

![browser-adapter](../../../assets/browser-adapter.gif)

## Running the `browser` Display Adapter Server

For configuration of the display adapter, check the main [README's configuration section](../../../README.md#configuration-options).

Startup of the script remains unchanged, just like with other display adapters. Additional command line flags work as usual.

After running your startup script, you should get a notice that your server is starting on your configured port. For the above example:

```
C:\Users\tyler\development\RGBMatrixEmulator\samples>python runtext.py
Press CTRL-C to stop sample
RGBME v0.6.0 - 32x32 Matrix | 1x1 Chain | 16px per LED (SQUARE) | BrowserAdapter
Starting server...
Server started and ready to accept requests on http://localhost:8888/
```

Once this is configured, your server is up and running and ready to accept requests on the configured port.

## Viewing the Emulator

### Via Websocket

By default, the server is configured to `http://localhost:8888/`. Simply navigate to this in the web browser of your choice and you should see streaming images once loaded.

If you've configured a custom port, you can navigate to the correct URL instead: `http://localhost:$PORT_NUMBER/`.

Once a browser is connected to the server, you will see the following message(s) in your terminal window:

```
WebSocket opened from: ::1
WebSocket opened from: 127.0.0.1
```

This indicates a successful connection has occurred.

### Via Static Image

:warning: **This functionality is experimental!** :warning:

The emulator also exposes static images in a format you configure. By default, the server is configured to expose this endpoint at `http://localhost:8888/image`.

This can be used to allow applications to poll the webserver for updated images or where a websocket is not applicable.

#### Tydbit Support

Tydbit requires `WebP` images to be exposed over a static HTTP endpoint. You can use the browser adapter's static image endpoint to provide cross-functional compatibility to Tydbit boards.

An example configuration that works for Tydbit matrices is provided:

```json
{
  "pixel_outline": 0,
  "pixel_size": 1,
  "pixel_style": "square",
  "display_adapter": "browser",
  "suppress_font_warnings": false,
  "suppress_adapter_load_errors": false,
  "browser": {
    "port": 8888,
    "target_fps": 24,
    "fps_display": false,
    "quality": 70,
    "image_border": true,
    "debug_text": false,
    "image_format": "WebP"
  },
  "log_level": "info"
}
```

## Error Handling

Exceptions in emulated Python scripts will cause the server to shut down. Fix the errors in the script before attempting to restart.

The Javascript client attempts to handle errors from the browser gracefully. If for some reason the socket is unable to fetch the next frame, it will retry the fetch every 6 seconds up to 10 times (for a total of 1 minute of retries). Once the max retry count is exhausted, it will stop retrying as there is likely another issue occurring.

You can view the errors via a console in the browser (which can be opened with hotkey `F12` or right click -> "Inspect").

## Known Issues

* A socket connection is never re-established when shutting down the server (either via `SIGINT` or unhandled exception) and restarting it before the client hits max retry count
* Excess blob references do not get cleaned up correctly in some instances, leading to memory leaks in some browsers
  * Main symptom appears to be a hanging browser when closing the emulator tab
