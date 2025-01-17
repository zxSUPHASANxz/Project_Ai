import cv2
from ultralytics import YOLO
import schedule
import time
import requests
from datetime import datetime
import threading

# โหลดโมเดล YOLOv8x
model = YOLO('yolov8x.pt')  # โหลดโมเดล YOLOv8x จากไฟล์ .pt

# ตัวแปรเก็บสถานะการทำงานและข้อมูลสถิติ
running = False
statistics = []

# ฟังก์ชันอ่านภาพจากกล้อง CCTV
def get_frame_from_cctv():
    cap = cv2.VideoCapture('rtsp://your_cctv_stream')  # แทนที่ด้วย URL กล้อง CCTV ของคุณ
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

# ฟังก์ชันตรวจจับอุบัติเหตุ
def detect_accident(frame):
    results = model(frame)  # ตรวจจับวัตถุในภาพ
    for result in results.xyxy[0]:
        # ตรวจจับวัตถุที่ตรงกับ "accident" หรือคลาสที่ต้องการ
        if int(result[-1]) == 1:  # ตัวอย่างคลาส (แก้ไขตาม Dataset)
            return True
    return False

# ฟังก์ชันส่งข้อความไปยัง Line
def send_line_notify(message, image_path=None):
    token = 'YOUR_LINE_NOTIFY_TOKEN'  # ใส่ Line Notify Token ของคุณ
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': message}
    files = {'imageFile': open(image_path, 'rb')} if image_path else None

    try:
        response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data, files=files)
        if response.status_code == 200:
            print(f"ส่งข้อความไปยัง Line สำเร็จ: {message}")
        else:
            print(f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}")
    except Exception as e:
        print(f"ข้อผิดพลาดในการส่ง Line Notify: {e}")

# ฟังก์ชันแจ้งเตือนทันทีเมื่อเกิดอุบัติเหตุ
def notify_accident_immediately(frame):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = f'accident_{timestamp.replace(" ", "_").replace(":", "-")}.jpg'
    cv2.imwrite(filename, frame)  # บันทึกภาพอุบัติเหตุ
    send_line_notify(f"แจ้งเตือนด่วน! ตรวจพบอุบัติเหตุเวลา {timestamp}", filename)

# ฟังก์ชันเก็บสถิติและแจ้งเตือน
def process_frame(frame):
    global statistics
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if detect_accident(frame):
        notify_accident_immediately(frame)
        statistics.append({'timestamp': timestamp, 'location': 'CCTV 1'})

# ฟังก์ชันเริ่มต้นการตรวจจับ
def start_detection():
    global running
    if running:
        print("ระบบกำลังทำงานอยู่แล้ว")
        return

    running = True
    print(f"เริ่มการตรวจจับ: {datetime.now()}")

    while running:
        try:
            frame = get_frame_from_cctv()
            if frame is not None:
                process_frame(frame)
            time.sleep(1)  # ลดการใช้งานทรัพยากร
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการตรวจจับ: {e}")

# ฟังก์ชันหยุดการตรวจจับ
def stop_detection():
    global running
    if not running:
        print("ระบบไม่ได้ทำงาน")
        return

    running = False
    print(f"หยุดการตรวจจับ: {datetime.now()}")
    send_daily_statistics()

# ฟังก์ชันส่งสถิติรายวันไปยัง Line
def send_daily_statistics():
    if statistics:
        message = f"สถิติรายวัน:\nตรวจพบอุบัติเหตุ {len(statistics)} ครั้ง\n"
        for i, event in enumerate(statistics, 1):
            message += f"{i}. เวลา: {event['timestamp']} ที่ {event['location']}\n"
        send_line_notify(message)
    else:
        send_line_notify("สถิติรายวัน: ไม่มีการตรวจพบอุบัติเหตุ")
    
    # ล้างสถิติสำหรับวันถัดไป
    statistics.clear()

# ตั้งเวลาเปิด-ปิดระบบอัตโนมัติ
def schedule_tasks():
    schedule.every().day.at("09:00").do(lambda: threading.Thread(target=start_detection).start())
    schedule.every().day.at("21:00").do(stop_detection)

# การทำงานหลักของ Scheduler
if __name__ == "__main__":
    print("เริ่มระบบจัดการเวลา...")
    schedule_tasks()
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("ระบบหยุดทำงาน")
            break
        except Exception as e:
            print(f"ข้อผิดพลาดใน Scheduler: {e}")
