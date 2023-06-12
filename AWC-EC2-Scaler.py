import cv2
from cvzone.HandTrackingModule import HandDetector
import boto3

def genOS():
    ec2=boto3.resource('ec2')
    instances= ec2.create_instances(MinCount=1, MaxCount=1, InstanceType="t2.medium", ImageId="ami-0f5ee92e2d63afc18", SecurityGroupIds=['sg-0717bcd480e5ef42b'])
    return instances[0].id
    
def delOS(id):
    ec2=boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=[id]).terminate()
    
detector = HandDetector(maxHands=1 , detectionCon=0.8 )
allOS=[]
cap = cv2.VideoCapture(0)

while True:
    ret,  photo = cap.read()
    hand = detector.findHands(photo , draw=False)
    if hand:
        detectHand = hand[0]
        if detectHand:
            fingerup = detector.fingersUp(detectHand)
            if detectHand['type'] == 'Left':
                for i in fingerup:
                    if i==1:
                        allOS.append(genOS())
            
            else:
                for i in fingerup:
                    if i==1:
                        delOS(allOS.pop())
            
    cv2.imshow("my photo", photo)
    if cv2.waitKey(2000) == 27:
        break
        
cv2.destroyAllWindows()
cap.release()


# https://www.section.io/engineering-education/creating-a-hand-tracking-module/
