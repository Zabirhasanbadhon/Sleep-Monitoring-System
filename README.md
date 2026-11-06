# 🛌 Sleep Monitoring System

<p align="center">
  <strong>AI-Powered Sleep Detection & Workplace Monitoring</strong>
  <br />
  Real-time computer vision system for detecting sleeping behavior using YOLO and Python.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/YOLOv8-Object%20Detection-purple" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv" />
  <img src="https://img.shields.io/badge/Tkinter-GUI-orange" />
  <img src="https://img.shields.io/badge/License-AGPL--3.0-red" />
</p>

---

## 📌 Overview

**Sleep Monitoring System** is an AI-powered computer vision application designed to detect and monitor sleeping behavior in workplace environments.

Built with **Python, YOLO, OpenCV, and Tkinter**, this application uses a custom-trained deep learning model to identify sleeping and active individuals through live webcam feeds or recorded video files.

The system detects sleeping postures, displays bounding boxes and labels, and generates annotated video recordings for further review.

### 🎯 Potential Applications

- 🏢 **Workplace Monitoring** — Monitor alertness in offices, control rooms, and security stations.
- 🎓 **Classroom Monitoring** — Identify sleeping behavior during lectures.
- 🚗 **Driver Fatigue Research** — Adapt the detection approach for driver drowsiness research.
- 📊 **Behavior Analysis** — Study sleep-related behavior in monitored environments.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎥 Real-Time Detection | Supports live webcam and prerecorded videos |
| 🤖 Custom YOLO Model | Uses trained `last.pt` model weights |
| 🎨 Detection Visualization | Displays bounding boxes and class labels |
| 🖥️ Interactive GUI | Simple Start and Stop controls using Tkinter |
| 💾 Video Recording | Saves annotated videos automatically |
| ⚡ Multithreading | Runs video processing without freezing the GUI |
| 📈 Live Status | Displays Ready, Loading, Monitoring, and Stopped states |
| 🎯 Two Detection Classes | Identifies `active` and `sleep` behaviors |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLOv8 / Ultralytics | Object detection and inference |
| OpenCV | Video capture and frame processing |
| Tkinter | Graphical user interface |
| Pillow | Image conversion and GUI display |
| Supervision | Bounding box and label annotation |
| Threading | Background video processing |
| PyResearch | Additional utility functions |

---

## 🖥️ How to Use

Follow these simple steps to start monitoring:

1. **Launch Application** — Run `Main.py` to open the GUI.
2. **Load Model** — Wait until the YOLO model finishes loading.
3. **Start Monitoring** — Click the Start Monitoring button.
4. **View Detection** — Watch the live video feed with bounding boxes and labels.
5. **Stop Monitoring** — Click the Stop Monitoring button.
6. **View Output** — Find the processed video saved as `output_sleep_monitor.mp4`.

### 📊 System Status

| Status | Description |
|---|---|
| 🟢 Ready | Application is initialized |
| 🟡 Loading | YOLO model is loading |
| 🔴 Monitoring | Video detection is running |
| ⚪ Stopped | Monitoring has ended |

---

## 🧠 Model Information

The application uses a custom-trained YOLO object detection model.

| Parameter | Details |
|---|---|
| Model File | `last.pt` |
| Base Model | YOLO11s (as configured for training) |
| Task | Object Detection |
| Detection Classes | `active`, `sleep` |
| Training Epochs | 25 |
| Image Size | 640 × 640 |
| Framework | Ultralytics |
| Model Format | PyTorch weights (`.pt`) |

### Detection Classes

The model identifies two primary classes:

- **Active:** An individual classified as awake or active.
- **Sleep:** An individual classified as sleeping.

### Detection Workflow

1. Capture a video frame from the webcam or video file.
2. Pass the frame to the trained YOLO model.
3. Detect objects and classify their behavior.
4. Draw bounding boxes and labels using Supervision.
5. Display the annotated frame in the Tkinter GUI.
6. Save processed frames to the output video.

---

## 🎬 Output Video

The application generates an annotated video:

```text
output_sleep_monitor.mp4
```

The output includes detected objects, bounding boxes, and class labels.

---

## 📸 Application Screenshots

Add your application screenshots to the `screenshots/` folder.

### 1. Application Interface

![Sleep Monitoring GUI](screenshots/gui_ready.png)

### 2. Live Sleep Detection

![Live Monitoring](screenshots/gui_monitoring.png)

### 3. Detection Output

![Detection Output](screenshots/output_sample.png)

---

## 🐛 Troubleshooting

### ❌ Supervision BoundingBoxAnnotator Error

**Error:**

```text
AttributeError: module 'supervision' has no attribute 'BoundingBoxAnnotator'
```

**Cause:** Different Supervision versions use different annotation APIs.

**Solution:** For versions where `BoxAnnotator` is the supported API, replace:

```python
self.bounding_box_annotator = sv.BoundingBoxAnnotator()
```

With:

```python
self.bounding_box_annotator = sv.BoxAnnotator()
```

Check the installed version and its API documentation before changing the code.

### ❌ Could Not Open Video File

**Possible causes:**

- Incorrect video file path.
- Missing video file.
- Unsupported video codec.
- Incorrect webcam index.

**Solution:**

For webcam:

```python
VIDEO_SOURCE = 0
```

For a video file:

```python
VIDEO_SOURCE = r"C:\path\to\your\video.mov"
```

### ❌ GUI Freezes During Detection

**Cause:** Heavy video processing is blocking the Tkinter main thread.

**Solution:** Run video inference in a background thread:

```python
threading.Thread(
    target=self.process_video,
    daemon=True
).start()
```

For safe Tkinter updates, schedule GUI changes through `root.after()` rather than updating widgets directly from the worker thread.

### ❌ Model File Not Found

**Error:**

```text
FileNotFoundError: last.pt
```

**Solution:** Verify that `last.pt` is in the same directory as `Main.py`, or configure the correct model path.

### ❌ Missing Python Packages

Install the dependencies:

```bash
pip install opencv-python pillow supervision ultralytics pyresearch
```

---

## 🔐 Privacy & Responsible Use

This project is intended for computer vision research, workplace safety demonstrations, and educational purposes.

- Obtain appropriate consent before monitoring individuals.
- Follow applicable privacy and workplace monitoring regulations.
- Secure recorded video files and restrict access.
- Avoid using automated predictions as the sole basis for employment or disciplinary decisions.
- Model predictions may be inaccurate and should be reviewed by a human.

---

## 🗺️ Future Improvements

- [ ] Sleep duration tracking
- [ ] Detection count dashboard
- [ ] Real-time alerts and notifications
- [ ] Detection history and reporting
- [ ] Multiple camera support
- [ ] Improved detection accuracy
- [ ] Exportable monitoring reports
- [ ] Web-based monitoring dashboard
- [ ] Model performance visualization

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome!

1. Fork this repository.
2. Create a new feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add new feature"
   ```

4. Push your branch:

   ```bash
   git push origin feature/your-feature
   ```

5. Open a Pull Request.

---

## 📄 License

This project uses a custom-trained YOLO model.

**Important:** Ultralytics licensing and your project's licensing are separate considerations. Ultralytics offers AGPL-3.0 and Enterprise licensing options. Check the applicable license terms for your use case before distributing the application.

If this repository is distributed under AGPL-3.0, include the appropriate `LICENSE` file and comply with its requirements.

---

## 🔗 Resources & References

- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [Roboflow Supervision](https://github.com/roboflow/supervision)
- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)

---

## 👨‍💻 Author

**ZaBir Hasan**

- Website: [www.zabirhasan.com](https://www.zabirhasan.com)

---

## 🙌 Acknowledgements

Special thanks to:

- [Ultralytics](https://github.com/ultralytics/ultralytics) — YOLO object detection framework.
- [Roboflow](https://roboflow.com/) — Supervision annotation library.
- [OpenCV](https://opencv.org/) — Computer vision tools.
- The Python open-source community ❤️

---

<p align="center">
  <strong>🛌 Sleep Monitoring System</strong>
  <br />
  AI-Powered Sleep Detection with Python & YOLO.
  <br /><br />
  <sub>Built with ❤️ by ZaBir</sub>
</p>
