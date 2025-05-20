import os
import pandas as pd
from PIL import Image
from analysis.ocr import extract_text
from analysis.color_analysis import analyze_colors

# 이미지 폴더 경로
IMAGE_FOLDER = 'images'

# 결과 저장용 리스트
data = []

# 이미지 폴더의 모든 파일을 처리
for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        path = os.path.join(IMAGE_FOLDER, filename)
        image = Image.open(path)

        # OCR 텍스트 추출
        text = extract_text(image)

        # 색상 분석
        colors = analyze_colors(image)
        color_str = ', '.join([f'{color}:{count}' for color, count in colors.items()])

        # 데이터 저장 (객체 인식은 제외)
        data.append({
            '이미지 이름': filename,
            '텍스트': text,
            '주요 색상': color_str
        })

# 결과를 Excel 파일로 저장
df = pd.DataFrame(data)
df.to_excel('analysis_result.xlsx', index=False)

print('분석 완료! 결과 파일: analysis_result.xlsx')
