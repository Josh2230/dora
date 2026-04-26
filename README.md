# dora-rs learning projects

A collection of small projects built while learning [dora-rs](https://dora-rs.ai) — a dataflow-oriented robotics framework for building modular, parallel pipelines in Python and Rust.

## What is dora-rs?

DORA (Dataflow-Oriented Robotic Architecture) is middleware that lets you build robotic applications as a graph of independent nodes that communicate through shared memory using Apache Arrow arrays. Each node runs as a separate process, making pipelines truly parallel and modular.

## Projects

### node_basics
Foundational exercises for understanding core DORA concepts — timers, error handling, and multi-input synchronization.

### data-and-arrow
Projects focused on data processing, Apache Arrow struct arrays, stateful computation, and CSV file logging.

### yolo-pipeline
A real-time computer vision pipeline using pre-built DORA community nodes for camera capture, YOLOv8 object detection, and live visualization with bounding boxes.

### wifi-radar
A passive WiFi radar that captures 802.11 probe requests to detect, fingerprint, and track nearby devices in real time

## Key Concepts Covered

- DORA node lifecycle (INPUT, STOP events)
- Apache Arrow arrays and struct arrays for passing typed data between nodes
- Dataflow YAML wiring — connecting node outputs to inputs
- Shared memory and zero-copy data passing between processes
- Stateful nodes maintaining state across events
- File I/O with proper flushing for data safety
- Error handling without crashing the pipeline
- Using pre-built community nodes from the dora-hub

## Setup

Each project has its own virtual environment:
```bash
cd my-dora-projects/
uv venv --seed -p 3.11
source .venv/bin/activate
dora run dataflow.yml --uv
```
