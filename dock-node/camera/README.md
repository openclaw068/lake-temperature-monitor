# Dock Camera (Pi Camera) → Home Assistant over HaLow

This assumes:
- Dock node is a **Raspberry Pi Zero 2 W**
- Camera is a **Pi Camera** connected via CSI
- Network uplink is via your **HaLow bridge** (dock Pi has normal IP connectivity)
- Home Assistant runs in a container at home

## Recommended approach: RTSP stream
Home Assistant ingests RTSP reliably (especially via go2rtc).

### Option 1 (recommended): MediaMTX (RTSP server) + Pi camera H.264

We’ll run **MediaMTX** on the dock Pi (RTSP server), and publish the camera stream to it.

1) Install camera tools:
```bash
sudo apt update
sudo apt install -y libcamera-apps
```

2) Start MediaMTX:
```bash
cd /opt/lake-temp/camera
# copy this repo folder's camera/ files here (or git clone the repo)

docker compose -f docker-compose.mediamtx.yml up -d
```

3) Publish a stream (starter command)

> Note: Pi camera streaming pipelines vary by OS and camera stack. This command is a known-good starting point for producing an H.264 stream; we’ll adjust it during bring-up if needed.

```bash
# Example: send H.264 over TCP to a local listener; MediaMTX then serves RTSP.
# If this exact command doesn't work on your Pi image, we'll swap to the correct libcamera pipeline.

libcamera-vid -t 0 --inline -n --width 1280 --height 720 --framerate 15 \
  --codec h264 --profile baseline --bitrate 800000 \
  -o - | nc -lk 127.0.0.1 8888
```

4) In Home Assistant / go2rtc, add:
- `rtsp://<dock-ip>:8554/lake`

## Home Assistant ingestion
If you run the go2rtc add-on (or go2rtc container), you can add:

- RTSP URL example: `rtsp://<dock-ip>:8554/cam`

If you don’t use go2rtc, HA can still ingest via Generic Camera/FFmpeg, but go2rtc is usually smoother.

## Power note
Live video means the dock node must be **always on**, so size solar/battery accordingly.
