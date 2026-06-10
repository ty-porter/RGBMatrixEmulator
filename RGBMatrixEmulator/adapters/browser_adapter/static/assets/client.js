(function () {
    const WS_RETRY_DELAY  = 2000; // milliseconds
    const FPS_DEFAULT     = 60;   // seconds
    const FPS_UPDATE_RATE = 300;  // milliseconds

    const canvas    = document.getElementById("liveImg");
    const ctx       = canvas.getContext("2d", { alpha: false });
    const fpsText   = document.getElementById("fps");
    const fpsTarget = parseInt(document.getElementById("targetFps").value) || FPS_DEFAULT;

    let startTime;
    let nFrames = 0;
    let fps = 0;

    let socket = generateSocket();

    function generateSocket() {
        let path = location.pathname;

        if (path.endsWith("index.html")) {
            path = path.substring(0, path.length - "index.html".length);
        }

        if(!path.endsWith("/")) {
            path = path + "/";
        }

        const wsProtocol = (location.protocol === "https:") ? "wss://" : "ws://";
        const ws = new WebSocket(wsProtocol + location.host + path + "websocket");

        ws.binaryType = 'arraybuffer';

        ws.onopen = function() {
            console.log("RGBME WebSocket connection established!");
            startTime = performance.now();
        };

        ws.onclose = function() {
            // Handle retries by recreating the connection to websocket.
            console.warn(`RGBME WebSocket connection lost. Retrying in ${WS_RETRY_DELAY / 1000}s.`)
            setTimeout(function() {
                // We generate socket with a timeout to make sure server has time to recover.
                socket = generateSocket();
            }, WS_RETRY_DELAY);
        }

        ws.onerror = function() {
            ws.close();
        }

        ws.onmessage = function(evt) {
            nFrames++;

            const blob = new Blob([evt.data], { type: IMAGE_MIME });
            createImageBitmap(blob).then((bitmap) => {
                if (canvas.width !== bitmap.width || canvas.height !== bitmap.height) {
                    canvas.width  = bitmap.width;
                    canvas.height = bitmap.height;
                }
                ctx.drawImage(bitmap, 0, 0);
                bitmap.close();
            }).catch(() => {});

            if (fpsText) {
                const endTime = performance.now();
                const deltaT = endTime - startTime;

                if (deltaT > FPS_UPDATE_RATE) {
                    fps = (nFrames / (deltaT / 1000)).toFixed(2);

                    fpsText.textContent = fps;

                    startTime = endTime;
                    nFrames = 0;
                }
            }
        };

        return ws;
    }

    console.log(`TARGET FPS: ${fpsTarget}`);
})();
