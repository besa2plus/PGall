# 🚀 PGall 기여 가이드

환영합니다! 이 문서는 오픈소스 기여가 처음인 분들을 위한 가이드입니다.

## 📋 목차
1. [프로젝트 시작하기](#프로젝트-시작하기)
2. [이슈 작성하기](#이슈-작성하기)
3. [코드 작성 및 커밋](#코드-작성-및-커밋)
4. [Pull Request 보내기](#pull-request-보내기)
5. [자주 묻는 질문](#자주-묻는-질문)
6. [추가 리소스](#-추가-리소스)

---

## 프로젝트 시작하기

### 전체 흐름 이해하기

오픈소스 프로젝트에 기여하려면 다음 3단계를 거칩니다:

```
[원본 저장소]  ----Fork---->  [내 GitHub 저장소]  ----Clone---->  [내 컴퓨터]
github.com/원본/PGall      github.com/나/PGall         C:/PGall/
        ↑                                                    |
        |                                                    |
        +----------------Pull Request-----------------------+
```

1. **Fork** (GitHub에서): 원본 저장소를 내 GitHub 계정으로 복사
2. **Clone** (로컬에서): 내가 Fork한 저장소를 내 컴퓨터로 다운로드
3. **Upstream 설정**: 원본 저장소의 최신 변경사항을 받아올 수 있도록 연결

> 💡 **왜 이렇게 해야 하나요?**  
> 원본 저장소에는 직접 Push할 권한이 없습니다. 그래서 내 계정에 복사본(Fork)을 만들고,  
> 그 복사본에서 작업한 후, Pull Request로 원본에 제안하는 방식으로 기여합니다.
>
> **간단히 말하면:**  
> Fork는 별개의 개념이지만, 오픈소스 기여 워크플로우에서는 "Fork → Clone → 작업(커밋 등) → Push → PR" 순서로 진행됩니다.

### 1. Fork 하기 (GitHub 웹에서)

**Fork**는 GitHub 서버에서 일어나는 작업입니다.

1. [PGall 저장소](https://github.com/[원본저장소]/PGall)로 이동
2. 우측 상단의 **Fork** 버튼 클릭
3. 본인의 GitHub 계정에 복사본이 생성됨

이제 `https://github.com/[본인아이디]/PGall` 저장소가 생겼습니다!

### 2. Clone 하기 (로컬 컴퓨터에서)

**Clone**은 GitHub 저장소를 내 컴퓨터로 다운로드하는 작업입니다.
```bash
# 본인의 fork한 저장소를 clone
git clone https://github.com/[본인아이디]/PGall.git

# 또는 SSH 사용 시
git clone git@github.com:[본인아이디]/PGall.git

# 프로젝트 폴더로 이동
cd PGall
```

### 3. Upstream 설정하기 (원본 저장소 연결)

**Upstream**은 원본 저장소를 가리키는 별칭입니다.

다른 사람이 원본 저장소에 변경사항을 추가하면, 내 Fork에는 자동으로 반영되지 않습니다.  
그러나 Upstream을 설정하면 원본의 최신 코드를 내 로컬로 가져올 수 있습니다.

```bash
# 원본 저장소를 upstream으로 추가
git remote add upstream https://github.com/[원본저장소]/PGall.git

# 확인
git remote -v
# origin    https://github.com/[본인아이디]/PGall.git (fetch)  ← 내 Fork
# origin    https://github.com/[본인아이디]/PGall.git (push)
# upstream  https://github.com/[원본저장소]/PGall.git (fetch)  ← 원본
# upstream  https://github.com/[원본저장소]/PGall.git (push)
```

**정리하면:**
- `origin`: 내가 Fork한 저장소 (여기에 Push 가능)
- `upstream`: 원본 저장소 (여기서 최신 코드를 받아옴)

---

## 이슈 작성하기

이슈는 걍 쓰고 싶을 때 쓰면 됩니다.
이슈란은 작업용이기도 하고, 커뮤니티 용이기도 합니다.

### 좋은 이슈 예시

#### 1. 새로운 도구 제안
```markdown
## 제목
[뉴비/주니어/시니어] 도구명 - 간단한 설명

## 설명
어떤 문제를 해결하는 도구인지 설명

## 구현 계획
- [ ] 기능 1
- [ ] 기능 2
- [ ] README 작성
- [ ] 테스트/실행 영상
```

#### 2. 버그 리포트
```markdown
## 제목
[버그] 간단한 버그 설명

## 재현 방법
1. 단계 1
2. 단계 2
3. 발생하는 오류

## 예상 동작
어떻게 동작해야 하는지

## 실제 동작
실제로 어떻게 동작하는지

## 환경
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- 관련 도구: 도구명 및 버전
```

---

## 코드 작성 및 커밋

### 1. 브랜치 생성

작업을 시작하기 전에 먼저 원본 저장소의 최신 코드를 받아와야 합니다.

```bash
# 1. upstream(원본 저장소)의 최신 변경사항 정보를 가져오기
git fetch upstream

# 2. 내 로컬의 main 브랜치로 이동
git checkout main

# 3. upstream의 main 브랜치 내용을 내 로컬 main에 합치기
git merge upstream/main

# 4. 새 브랜치 생성 및 이동
git checkout -b feature/내-도구-이름
```

**각 명령어 설명:**
- `git fetch upstream`: 원본 저장소의 최신 커밋 정보를 다운로드 (실제 파일은 아직 변경 안 됨)
- `git checkout main`: main 브랜치로 이동
- `git merge upstream/main`: 원본의 최신 코드를 현재 브랜치에 병합 (실제 파일이 업데이트됨)
- `git checkout -b 브랜치명`: 새 브랜치를 만들고 그 브랜치로 이동

> 💡 **fetch vs pull, 뭐가 다른가요?**  
> - `git fetch`: 원격 저장소의 변경사항을 다운로드만 함 (병합 안 함)
> - `git pull`: 변경사항을 다운로드하고 자동으로 병합함 (fetch + merge를 한 번에)
> 
> 위 예시에서는 `fetch` → `merge`로 나눠서 진행합니다.  
> `git pull upstream main`으로 한 번에 할 수도 있지만, 초보자는 단계별로 하는 게 안전합니다.

> 💡 **왜 이렇게 해야 하나요?**  
> 다른 사람이 원본에 추가한 최신 코드를 받지 않고 작업하면,  
> 나중에 PR을 보낼 때 충돌(conflict)이 발생할 수 있습니다.

### 2. 작업 디렉토리 구조
```
PGall/
├── tools/
│   └── [본인아이디]-[도구명]/
│       ├── README.md          # 필수: 사용법, 실행방법
│       ├── src/               # 소스 코드
│       ├── examples/          # 예제 파일들
│       ├── screenshots/       # 스크린샷/GIF
│       └── requirements.txt   # 의존성 (언어에 따라)
```

### 3. README 작성 (필수!)
도구의 README.md에 반드시 포함해야 할 내용:
```markdown
# 도구명

## 문제
어떤 문제를 해결하는가?

## 해결
어떻게 해결하는가?

## 실행 방법
### 설치
\```bash
# 의존성 설치 명령어
\```

### 사용법
\```bash
# 실행 명령어 예시
\```

## 실행 결과
![스크린샷](./screenshots/demo.gif)
또는 설명

## 구조
간단한 구조 설명
```

### 4. 커밋하기 (중요: DCO 서명 필수!)
```bash
# 변경사항 확인
git status

# 파일 추가
git add .

# DCO 서명과 함께 커밋 (-s 옵션 필수!)
git commit -s -m "feat: 이미지 리사이저 추가"

# 또는 여러 줄 메시지
git commit -s -m "feat: 이미지 리사이저 추가

- PNG, JPG, WebP 지원
- 비율 유지 옵션 추가
- CLI 인터페이스 구현"
```

**⚠️ 중요**: 반드시 `-s` 옵션을 사용해서 `Signed-off-by`를 추가해야 합니다!

### 5. 커밋 메시지 규칙
```
feat: 새로운 도구/기능 추가
fix: 버그 수정
docs: 문서 수정
refactor: 코드 리팩토링
test: 테스트 추가
chore: 빌드/설정 관련
```

---

## Pull Request 보내기

### 1. Push 하기
```bash
# 본인의 fork한 저장소로 push
git push origin feature/내-도구-이름
```

### 2. PR 생성
1. GitHub에서 본인의 fork한 저장소로 이동
2. "Compare & pull request" 버튼 클릭
3. PR 템플릿 작성

### 3. PR 템플릿 예시
```markdown
## 무엇을 만들었나요?
간단한 설명

## 스킬 레벨
- [ ] 뉴비
- [ ] 주니어  
- [ ] 시니어

## 체크리스트
- [ ] README.md 작성 (문제/해결/실행방법/구조)
- [ ] 실행 결과 증빙 (스크린샷/GIF/영상)
- [ ] DCO 서명 완료 (git commit -s)
- [ ] 코드가 정상 동작함

## 스크린샷/데모
![데모](링크)
```

### 4. 리뷰 받기
- 리뷰어의 피드백에 답변하기
- 수정 요청이 있으면 코드 수정 후 다시 push
- 같은 브랜치에 push하면 PR에 자동으로 반영됨

---

## 자주 묻는 질문

### Q1. Fork? Clone? 차이가 뭔가요?

**Fork (GitHub 웹에서 하는 작업)**
- 원본 저장소를 내 GitHub 계정으로 복사
- GitHub 서버에서 일어나는 일
- 결과: `github.com/원본계정/PGall` → `github.com/내계정/PGall`

**Clone (로컬에서 하는 작업)**
- GitHub 저장소를 내 컴퓨터로 다운로드
- 내 컴퓨터에 파일로 저장됨
- 결과: `github.com/내계정/PGall` → `C:/내컴퓨터/PGall`

**비유하면:**
- Fork = 인터넷에 있는 남의 구글 드라이브 폴더를 내 구글 드라이브로 복사
- Clone = 내 구글 드라이브 파일을 내 컴퓨터로 다운로드

### Q2. 커밋을 잘못했어요!
```bash
# 마지막 커밋 메시지 수정
git commit --amend -s

# 마지막 커밋 취소 (변경사항은 유지)
git reset --soft HEAD~1

# 특정 파일만 unstage
git restore --staged 파일명
```

### Q3. fetch와 pull의 차이가 뭔가요?

**git fetch (다운로드만)**
- 원격 저장소의 변경사항을 가져오기만 함
- 내 작업 파일은 변경되지 않음
- 안전하게 최신 상태를 확인 가능

**git pull (다운로드 + 병합)**
- 원격 저장소의 변경사항을 가져와서 자동으로 병합
- `git fetch` + `git merge`를 한 번에 실행
- 빠르지만 충돌 가능성 있음

**추천:**
```bash
# 안전한 방법 (단계별)
git fetch upstream
git checkout main
git merge upstream/main

# 빠른 방법 (한 번에)
git pull upstream main
```

### Q4. upstream/main의 최신 코드를 받으려면?
```bash
# 방법 1: fetch + merge (권장)
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 방법 2: pull (빠름)
git pull upstream main
git push origin main
```

### Q5. 작업 중인 브랜치를 최신 코드에 맞추려면?
```bash
# 방법 1: merge
git checkout feature/내-브랜치
git merge upstream/main

# 방법 2: rebase (커밋 히스토리를 깔끔하게)
git checkout feature/내-브랜치
git rebase upstream/main
```

### Q6. DCO 서명을 까먹었어요!
```bash
# 마지막 커밋에 서명 추가
git commit --amend -s --no-edit

# 여러 커밋에 서명 추가 (마지막 3개 커밋)
git rebase HEAD~3 --signoff
```

### Q7. 어떤 도구를 만들어야 할지 모르겠어요
- README의 예시를 참고하세요
- 평소 불편했던 반복 작업을 자동화해보세요
- 이슈를 확인해서 아이디어를 얻으세요

### Q8. 실력이 부족한 것 같아요
- 뉴비 레벨부터 시작하세요!
- 단순한 도구도 충분히 가치있습니다
- 다른 사람의 PR을 보고 배우세요

---

## 🎉 추가 리소스

### Git 학습 자료
- [Git 공식 문서 (한글)](https://git-scm.com/book/ko/v2)
- [GitHub Docs (한글)](https://docs.github.com/ko)
- [Learn Git Branching](https://learngitbranching.js.org/?locale=ko) - 인터랙티브 튜토리얼

### 개발 도구
- [Visual Studio Code](https://code.visualstudio.com/) - 무료 에디터
- [GitHub Desktop](https://desktop.github.com/) - GUI Git 클라이언트
- [GitKraken](https://www.gitkraken.com/) - 고급 Git GUI

### 커뮤니티
- Issues 탭에서 질문하기
- Discussions (있다면)에서 논의하기
- 다른 기여자들의 코드 리뷰 보기

---

**기여해주셔서 감사합니다! 🙌**

문의사항이 있으면 언제든지 Issue를 열어주세요.

