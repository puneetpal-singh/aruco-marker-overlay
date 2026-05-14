# ArUco Marker Overlay

Computer-vision utility that detects ArUco markers in images and overlays a poster or planar graphic onto each marker using homography-based perspective warping.

## What It Demonstrates

- ArUco marker detection with OpenCV
- Corner extraction and marker-local coordinate handling
- Homography estimation for perspective-correct image overlay
- Batch image processing for repeatable visual output

## Typical Workflow

```powershell
python main.py `
  --input-dir "path\to\input-images" `
  --poster "path\to\poster.jpg" `
  --output-dir "path\to\outputs"
```

## Repository Scope

This repository keeps the overlay script and project structure lightweight. Input images, generated outputs, and local data folders are intentionally excluded from Git.

## Skills Shown

`Python` | `OpenCV` | `ArUco` | `Homography` | `Perspective Transform` | `Image Processing`
