#!/bin/bash
# set -e: 스크립트 실행 중 오류 발생 시 즉시 중단
set -e

# 1. 가상환경 생성 (없을 경우)
if [ ! -d ".venv" ]; then
    echo "가상환경(.venv)을 생성합니다..."
    python3.10 -m venv .venv
fi

# 2. 의존성 설치
echo "의존성을 설치합니다..."
.venv/bin/pip install -r requirements.txt
