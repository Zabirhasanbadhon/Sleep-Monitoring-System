import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import supervision as sv
from ultralytics import YOLO
import threading
import time

# --- Configuration ---
MODEL_PATH = "last.pt"       # Your trained sleep detection model
VIDEO_SOURCE = r"C:\Users\ZaBir\Desktop\Sleep Monitoring System\Sleeping in Office.mp4" # Replace with 0 for webcam
OUTPUT_FILE = "output_sleep_monitor.mp4"

class SleepMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZaBir | Sleep Monitoring System")
        self.root.geometry("1000x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # State variables
        self.is_running = False
        self.cap = None
        self.out = None
        self.model = None

        # Build UI
        self.create_widgets()
        self.load_model()

    def create_widgets(self):
        # Main frame for video
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.video_label = ttk.Label(self.video_frame)
        self.video_label.pack()

        # Control frame
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(pady=5, fill=tk.X, padx=10)

        self.start_btn = ttk.Button(self.control_frame, text="▶ Start Monitoring", command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(self.control_frame, text="⏹ Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(self.control_frame, text="Status: Ready", foreground="blue")
        self.status_label.pack(side=tk.RIGHT, padx=5)

    def load_model(self):
        try:
            self.status_label.config(text="Status: Loading model...", foreground="orange")
            self.root.update()
            self.model = YOLO(MODEL_PATH)
            self.status_label.config(text="Status: Model loaded", foreground="green")
        except Exception as e:
            self.status_label.config(text="Status: Model load failed", foreground="red")
            messagebox.showerror("Model Error", f"Could not load model:\n{e}")

    def start_monitoring(self):
        if self.model is None:
            messagebox.showerror("Error", "Model not loaded.")
            return

        self.cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open video source.")
            return

        # Get video properties
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps == 0 or fps != fps: # Handle invalid FPS
            fps = 25.0

        # Initialize VideoWriter (optional recording)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(OUTPUT_FILE, fourcc, fps, (width, height))

        # Initializers for Supervision annotators
        self.bounding_box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Monitoring...", foreground="green")

        # Start processing in a separate thread to keep GUI responsive
        self.thread = threading.Thread(target=self.process_video, daemon=True)
        self.thread.start()

    def process_video(self):
        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Run inference
            results = self.model(frame, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(results)

            # Create labels for Supervision
            labels = [
                results.names[class_id]
                for class_id
                in detections.class_id
            ]

            # Annotate
            annotated_frame = self.bounding_box_annotator.annotate(
                scene=frame.copy(), detections=detections)
            annotated_frame = self.label_annotator.annotate(
                scene=annotated_frame, detections=detections, labels=labels)

            # Write to file
            if self.out is not None:
                self.out.write(annotated_frame)

            # Convert to RGB and resize for Tkinter display
            rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            # Resize to fit window (optional, maintains aspect ratio)
            display_width = 900
            display_height = 600
            rgb_image = cv2.resize(rgb_image, (display_width, display_height))
            
            img_pil = Image.fromarray(rgb_image)
            img_tk = ImageTk.PhotoImage(image=img_pil)

            # Update GUI (schedule on main thread)
            self.root.after(0, self.update_frame, img_tk)

            # Control frame rate roughly
            time.sleep(0.01)

        # Cleanup when loop exits
        self.root.after(0, self.stop_monitoring)

    def update_frame(self, img_tk):
        if self.is_running:
            self.video_label.imgtk = img_tk
            self.video_label.configure(image=img_tk)

    def stop_monitoring(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", foreground="blue")

        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if self.out is not None:
            self.out.release()
            self.out = None

    def on_close(self):
        self.stop_monitoring()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SleepMonitorApp(root)
    root.mainloop()
