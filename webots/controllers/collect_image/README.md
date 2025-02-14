
# collect_image

Webots controller for the SUSTAINA-OP proto model.  
This controller adds an image-saving feature to the [SUSTAINA-OP_walking](https://github.com/SUSTAINA-OP/SUSTAINA-OP_Webots/tree/master/webots/controllers/SUSTAINA-OP_walking).

---

## 👀Emvironment
- webots R2023b
- python3.8 or later
---

## ⚙️Installation

Install required packages using pip.

```bash
  pip3 install -r requirements.txt
```
## Docker
```bash
docker build -t collect_image_env -f Docker/Dockerfile .
## start container
./launch_container.sh
```

---  
## 🧬Features

### [SUSTAINA-OP_webots](https://github.com/SUSTAINA-OP/SUSTAINA-OP_Webots/tree/master/webots/controllers/SUSTAINA-OP_walking)
- Sending walking direction by zmq and protobuf message.
- Get image data from camera.
- Viewing image from camera.

---  
## Collect Image
- Start "[collect_image.wbt](https://github.com/RikuYokoo/SUSTAINA-OP_Webots/blob/master/webots/world/collect_image.wbt)" and watch the robot move toward the ball.
- Reposition the other three robots manually.
- Move the ball so the robot will follow it and capture various images.
## ⚡️Example

### CLI

#### **Viewing image from camera**
```bash
python3 view_image.py
```
--- 

## 🧾License

[apache license 2.0](https://www.apache.org/licenses/LICENSE-2.0)
