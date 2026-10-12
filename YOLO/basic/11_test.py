import cv2
from ultralytics import YOLO

model = YOLO('best.pt')

cap = cv2.VideoCapture(0) # ('data/mouse.mp4')

if not cap.isOpened():
	print('카메라 이상으로 시작할 수 없습니다.')
	exit()

while True:
	success,frame = cap.read()
	
	if not success:
		break
		
	results = model.predict(
		frame,
		conf=0.1,
		imgsz=[640,480],
		show=False,
		verbose=False,
		classes=[0]
	)
	
	yolo_frame = results[0].plot()
	resize_frame = cv2.resize(yolo_frame,(640,480))
	cv2.imshow('mouse detect',resize_frame)
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
cap.release()
cv2.destroyAllWindows()