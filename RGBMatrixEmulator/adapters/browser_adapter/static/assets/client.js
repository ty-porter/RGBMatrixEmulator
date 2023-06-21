function init() {
    const WS_RETRY_DELAY = 2000;
    const FPS_DEFAULT    = 24;

    let img       = document.getElementById("liveImg");
    let fpsText   = document.getElementById("fps");
    let fpsTarget = parseInt(document.getElementById("targetFps").value) || FPS_DEFAULT;

    let requestStartTime = performance.now();
    let startTime = performance.now();
    let time = 0;
    let requestTime = 0;
    let timeSmoothing = 0.9;           // larger=more smoothing
    let requestTimeSmoothing = 0.2;    // larger=more smoothing
    let targetTime = 1000 / fpsTarget;

    let socket = generateSocket();

    function requestImage() {
        requestStartTime = performance.now();
        socket.send('more');
    }

    function generateSocket() {
        let path = location.pathname;

        if (path.endsWith("index.html")) {
            path = path.substring(0, path.length - "index.html".length);
        }

        if(!path.endsWith("/")) {
            path = path + "/";
        }

        let wsProtocol = (location.protocol === "https:") ? "wss://" : "ws://";
        let ws = new WebSocket(wsProtocol + location.host + path + "websocket");

        ws.binaryType = 'arraybuffer';

        ws.onopen = function() {
            console.log("RGBME WebSocket connection established!");
            startTime = performance.now();
            requestImage();
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
            let arrayBuffer = evt.data;
            let blob  = new Blob([new Uint8Array(arrayBuffer)], {type: "image/jpeg"});
            let old_img = img.src.slice()
            img.src   = window.URL.createObjectURL(blob);
            window.URL.revokeObjectURL(old_img);

            let endTime = performance.now();
            let currentTime = endTime - startTime;
            // smooth with moving average
            time = (time * timeSmoothing) + (currentTime * (1.0 - timeSmoothing));
            startTime = endTime;
            let fps = Math.round(1000 / time);

            if (fpsText) {
                fpsText.textContent = fps;
            }

            let currentRequestTime = performance.now() - requestStartTime;
            // smooth with moving average
            requestTime = (requestTime * requestTimeSmoothing) + (currentRequestTime * (1.0 - requestTimeSmoothing));
            let timeout = Math.max(0, targetTime - requestTime);

            setTimeout(requestImage, timeout);
        };

        return ws;
    }

    console.log(`TARGET FPS: ${fpsTarget}`);
};

init();
