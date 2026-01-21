# TripoSR <a href="https://huggingface.co/stabilityai/TripoSR"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Model_Card-Huggingface-orange"></a> <a href="https://huggingface.co/spaces/stabilityai/TripoSR"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Gradio%20Demo-Huggingface-orange"></a> <a href="https://huggingface.co/papers/2403.02151"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Paper-Huggingface-orange"></a> <a href="https://arxiv.org/abs/2403.02151"><img src="https://img.shields.io/badge/Arxiv-2403.02151-B31B1B.svg"></a> <a href="https://discord.gg/mvS9mCfMnQ"><img src="https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white"></a>

<div align="center">
  <img src="figures/teaser800.gif" alt="티저 영상">
</div>

**TripoSR**은 단일 이미지에서 **빠른** 피드포워드 3D 재구성을 위한 최첨단 오픈소스 모델의 공식 코드베이스입니다. [Tripo AI](https://www.tripo3d.ai/)와 [Stability AI](https://stability.ai/)가 공동으로 개발했습니다.
<br><br>
[Large Reconstruction Model (LRM)](https://yiconghong.me/LRM/)의 원리를 활용하여, TripoSR은 3D 재구성의 속도와 품질을 크게 향상시키는 핵심 발전을 이루었습니다. 이 모델은 NVIDIA A100 GPU에서 0.5초 이내에 고품질 3D 모델을 생성하는 빠른 입력 처리 능력이 특징입니다. TripoSR은 정성적 및 정량적 평가 모두에서 우수한 성능을 보여주었으며, 여러 공개 데이터셋에서 다른 오픈소스 대안들을 능가했습니다. 아래 그림은 TripoSR의 성능을 다른 주요 모델들과 비교한 시각적 비교 및 메트릭을 보여줍니다. 모델 아키텍처, 학습 과정 및 비교에 대한 자세한 내용은 이 [기술 보고서](https://arxiv.org/abs/2403.02151)에서 확인할 수 있습니다.

<!--
<div align="center">
  <img src="figures/comparison800.gif" alt="티저 영상">
</div>
-->
<p align="center">
    <img width="800" src="figures/visual_comparisons.jpg"/>
</p>

<p align="center">
    <img width="450" src="figures/scatter-comparison.png"/>
</p>


이 모델은 MIT 라이선스로 배포되며, 소스 코드, 사전 학습된 모델 및 인터랙티브 온라인 데모가 포함됩니다. 우리의 목표는 연구자, 개발자 및 크리에이터들이 3D 생성 AI와 3D 콘텐츠 제작의 가능성을 넓힐 수 있도록 지원하는 것입니다.

## 시작하기
### 설치
- Python >= 3.8
- CUDA가 사용 가능한 경우 설치
- 플랫폼에 맞게 PyTorch 설치: [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/) **[로컬에 설치된 CUDA 메이저 버전이 PyTorch에 포함된 CUDA 메이저 버전과 일치하는지 확인하세요. 예를 들어 CUDA 11.x가 설치되어 있다면, CUDA 11.x로 컴파일된 PyTorch를 설치해야 합니다.]**
- setuptools 업데이트: `pip install --upgrade setuptools`
- 기타 종속성 설치: `pip install -r requirements.txt`

### 수동 추론
```sh
python run.py examples/chair.png --output-dir output/
```
재구성된 3D 모델이 `output/`에 저장됩니다. 공백으로 구분하여 여러 이미지 경로를 지정할 수도 있습니다. 기본 옵션은 단일 이미지 입력에 약 **6GB VRAM**이 필요합니다.

정점 색상 대신 텍스처를 출력하려면 `--bake-texture` 옵션을 사용하세요. 출력 텍스처의 해상도(픽셀)를 지정하려면 `--texture-resolution`을 사용할 수도 있습니다.

이 스크립트의 자세한 사용법은 `python run.py --help`를 사용하세요.

### 로컬 Gradio 앱
```sh
python gradio_app.py
```

#### Anaconda 환경에서 실행
```sh
# Anaconda Prompt에서 실행
conda activate tripo_conda
cd C:\Users\SSPLUS\Documents\TripoSR
python gradio_app.py
```

## 문제 해결
> AttributeError: module 'torchmcubes_module' has no attribute 'mcubes_cuda'

또는

> torchmcubes was not compiled with CUDA support, use CPU version instead.

이는 `torchmcubes`가 CUDA 지원 없이 컴파일되었기 때문입니다. 다음 사항을 확인하세요:

- 로컬에 설치된 CUDA 메이저 버전이 PyTorch에 포함된 CUDA 메이저 버전과 일치해야 합니다. 예를 들어 CUDA 11.x가 설치되어 있다면, CUDA 11.x로 컴파일된 PyTorch를 설치해야 합니다.
- `setuptools>=49.6.0`이어야 합니다. 그렇지 않으면 `pip install --upgrade setuptools`로 업그레이드하세요.

그런 다음 `torchmcubes`를 다시 설치합니다:

```sh
pip uninstall torchmcubes
pip install git+https://github.com/tatsy/torchmcubes.git
```

## 인용
```BibTeX
@article{TripoSR2024,
  title={TripoSR: Fast 3D Object Reconstruction from a Single Image},
  author={Tochilkin, Dmitry and Pankratz, David and Liu, Zexiang and Huang, Zixuan and and Letts, Adam and Li, Yangguang and Liang, Ding and Laforte, Christian and Jampani, Varun and Cao, Yan-Pei},
  journal={arXiv preprint arXiv:2403.02151},
  year={2024}
}
```
