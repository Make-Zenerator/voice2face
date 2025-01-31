
  

# 🔊 Voice2Face-Data

  

<img  src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img  src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"> <img  src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> <img  src="https://img.shields.io/badge/NCP-03C75A?style=for-the-badge&logo=Naver&logoColor=white"> <img  src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=Linux&logoColor=white"> <img  src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white"> <img  src="https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=Numpy&logoColor=white"> <img  src="https://img.shields.io/badge/Pytorch-EE4C2C?style=for-the-badge&logo=Pytorch&logoColor=white"> <img  src="https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=FFmpeg&logoColor=white">



## Project Structure

```
code
┣ audio
┃ ┣ audio_check_dB.py
┃ ┣ audio_crop.py
┃ ┣ audio_remove_noise.py
┃ ┣ audio_to_mfcc.py
┃ ┗ audio_wav_cropping.py
┣ crawling
┃ ┣ crawling_detect.py
┃ ┣ crawling_rename_video.py
┃ ┣ crawling_select_csv.py
┃ ┣ crawling_urlsave.py
┃ ┗ crawling_videosave.py
┣ EDA
┃ ┣ EDA_deepfake.ipynb
┃ ┣ EDA_HQvoxceleb.ipynb
┃ ┣ EDA_OLKAVS.ipynb
┃ ┗ EDA_survey.ipynb
┣ image
┃ ┣ image_clipseg2.py
┃ ┗ image_face_frame.py
┣ preprocess
┃ ┣ preprocess_file_tree_csv.py
┃ ┗ preprocess_image_gender_csv.py
┣ relabel
┃ ┣ relabel_detect_getframe.py
┃ ┣ relabel_select_csv.py
┃ ┗ relabel_Vox_age.py
┣ total
┃ ┣ total_audio_video_image.py
┃ ┗ total_origin_remove.py
┗ video
  ┣ video_clipimage.py
  ┗ video_download.py
┗ README.md
┗ requirements.txt
┗ airflow_docker 
┗ Dockerfile
...
```
## Usage

  

#### audio
 - `audio_check_dB.py`: 특정 dB 값을 확인하여 사람의 음성 여부를 판별하는 스크립트입니다.
 - `audio_dB_crop.py`: 오디오 파일에서 인간의 목소리 세그먼트를 추출하고 감지된 음성 세그먼트를 포함하는 새로운 오디오 파일을 10초로 자르는 스크립트입니다.
 - `audio_remove_noise.py`: 오디오 파일에서 음성을 분리한 후 노이즈를 줄이고 증폭하하는 스크립트 입니다.
 - `audio_to_mfcc.py`: 오디오 파일을 MFCC 이미지로 변환하여 저장하는 스크립트 입니다.
 - `audio_wav_cropping.py`: JSON POINT에 맞춰 오디오를 자르는 스크립트입니다.

#### crawling

 - `crawling_detect.py`: 비디오 클립에서 얼굴과 오디오를 감지하고 세분화하는 스크립트입니다.
 - `crawling_rename_video.py`: 'download' 폴더에서 비디오 이름과 CSV의 인덱스를 맞추는 스크립트입니다.
 - `crawling_select_csv.py`: 주어진 CSV 파일에서 YouTube ID를 찾아 해당하는 파일 이름에서 정보를 추출하고, 이 정보를 새로운 CSV 파일에 저장하는 간단한 데이터 처리 작업을 수행하는 스크립트입니다.
 - `crawling_urlsave.py`: Selenium을 사용하여 YouTube 크롤링을 수행하여 약 162개의 비디오에 대한 이름, 제목 및 URL 정보를 Youtube_search_df.csv에 저장하는 스크립트입니다.
 - `crawling_videosave.py`: '`crawling_urlsave.py`'를 통해 얻은 URL에서 비디오를 다운로드하는 스크립트입니다. 비디오는 'download' 폴더에 저장됩니다.

#### EDA 
 - `EDA_deepfake.ipynb`: '딥페이크 변조 영상' 데이터셋 metadata를 통한 EDA 스크립트입니다.
 - `EDA_HQvoxceleb.ipynb`: 'HQ-Voxceleb' 데이터셋 metadata를 통한 EDA 스크립트입니다.
 - `EDA_OLKAVS.ipynb`: 'OLKAVS' 데이터셋 metadata, voice를 통한 EDA 스크립트입니다.
 - `EDA_survey.ipynb`: 서비스 이용자를 대상으로 진행한 설문조사 EDA 스크립트입니다.

#### image

 - `image_clipseg2.py`: CLIPSeg 모델을 사용하여 텍스트 프롬프트를 기반으로 이미지 세분화를 수행하는 스크립트입니다. 이미지를 불러와 텍스트 프롬프트로 처리하고, 식별된 객체를 기반으로 세분화된 이미지를 생성합니다.
 - `image_face_frame.py`: 비디오에서 사람의 얼굴이 정면이고, 눈을 뜨고 있을 때 캡쳐하고 배경을 제거하는 스크립트입니다.


#### preprocess
 - `preprocess_file_tree_csv.py`: OLKAVS 데이터셋 전체를 학습(train), 검증(validation), 테스트(test) 3가지로 나눈 후, 각 데이터셋의 정보를 CSV 파일로 저장하는 스크립트입니다.
 - `preprocess_image_gender_csv.py`: 이미지 경로와 성별 데이터를 매칭해 csv 파일로 저장하는 스크립트입니다.

#### relabel

 - `relabel_detect_getframe.py`: 주어진 비디오에서 얼굴을 감지하고, 감지된 얼굴에 대해 성별과 연령을 추정하여 화면에 표시하고, 일정한 간격으로 프레임을 캡처하여 이미지 파일로 저장하는 기능을 수행합니다.
 - `relabel_select_csv.py`: 데이터 경로에서 YouTube ID를 추출하고, 파일 이름에서 필요한 정보를 추출하여 새로운 CSV 파일에 저장하는 스크립트입니다.
 - `relabel_Vox_age.py`: 이미지 폴더에서 이미지들을 읽어와 각 이미지의 나이를 예측하고, 가장 흔한 나이 그룹을 세서 출력하고, 그 결과를 CSV 파일에 저장하는 작업을 수행합니다.

#### video

 - `video_clipimage.py`: 주어진 이미지에서 얼굴을 감지하고, 감지된 얼굴 영역을 사각형으로 표시한 후 해당 얼굴을 256x256 크기로 조정하여 저장하는 작업을 수행합니다.
 - `video_download.py`: 주요 기능은 주어진 YouTube 비디오 링크에서 비디오를 다운로드하고, 다운로드한 비디오를 mp4 또는 mp3 형식으로 변환하는 스크립트입니다.

#### total
-   `total_audio_video_image.py`: 오디오, 비디오 및 이미지와 관련된 작업을 총 수행하는 스크립트입니다.
-   `total_origin_remove.py`: 데이터 경로에서 원본 파일을 제거하는 스크립트입니다.


  

## Getting Started

  
### Setting up Virtual Environment

  
1. Initialize and update the server

```

su -

source .bashrc

```

  

2. Create and Activate a virtual environment in the project directory

  

```

conda create -n env python=3.8

conda activate env

```

  

4. To deactivate and exit the virtual environment, simply run:

  

```

deactivate

```

  

### Install Requirements

  

To Install the necessary packages listed in `requirements.txt`, run the following command while your virtual environment is activated:

```

pip install -r requirements.txt

```

  
  
## Links
- [Naver BoostCamp 6th github](https://github.com/boostcampaitech6/level2-3-cv-finalproject-cv-08)
