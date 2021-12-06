# FontImgGenerateWithAug

특정 폰트를 사용하여 원하는 문장이나 단어를 Augmentation 기법을 적용시켜서 글자 인식 학습용 데이터로 생성

## How to use

## Input -> Output

2차원 or 3차원 -> 3차원

```python
python generate.py -d dictionary.txt -f fonts.yaml -a augments.yaml -o output
```

## Arguments

-   `-d`: 생성할 문장 혹은 단어들, 기본값
-   `-f`: 사용될 폰트의 list와 위치를 지정한 yaml 파일, 기본값 : assets/yamls/fonts.yaml
-   `-a`: 사용될 Augmentation 기법의 list와 비율을 지정한 yaml 파일 : assets/yamls/augments.yaml
-   `-o`: 결과물이 저장될 폴더의 이름 : results

## Links

-   Augmentation : https://github.com/NVlabs/ocrodeg
-   FontImage생성 : https://blog.naver.com/PostView.nhn?blogId=monkey5255&logNo=221594654820&parentCategoryNo=&categoryNo=72&viewDate=&isShowPopularPosts=true&from=search
-   한국인 이름 : https://koreanname.me/
-   한국 도로명 : https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=mainJusoDb
