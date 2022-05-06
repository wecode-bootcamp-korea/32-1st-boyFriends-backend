# 32th 라인프렌즈 스토어 프로젝트 - BoyFriends

## introduce

- 라인프렌즈 스토어 클론 프로젝트
- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인/기획 부분만 클론했습니다.
- 개발은 초기 세팅부터 전부 직접 구현했으며, 아래 데모 영상에서 보이는 부분은 모두 백앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발했습니다.
- 목업 데이터의 중요성을 개발자 시연 영상을 통해 뼈저리게 느꼈습니다.

### 팀원

- FE: 서성용, 안훈기, 전형준, 황석영
- BE: 송재관, 지기성

#### 기술 스택

- `FE`: JavaScript React.js, HTML5, CSS, SASS, react-router

- `BE`: Django, Python, MySQL, JWT, Bcrypt

#### Colaboration Tool

- Notion, Git, Trello, Slack, Google spread Sheet

---

### 데모 영상

https://youtu.be/7dLoURqLBgs

---

### 구현 기능

- 네브바

```
   - 상단 버튼을 이용한 라우팅 ( 로그인, 회원가입, 로그아웃 )
   - 토큰 존재 유무에 따른 버튼 렌더링 분화. ( 로그인, 회원가입 또는 로그아웃 )
   - localStorage 토큰 삭제를 통한 로그아웃
   - 검색 및 필터링 가능
   - 드롭다운 메뉴바 구성
   - outlet 기능을 이용해서, 특정 페이지에서만 출력
```

![](https://velog.velcdn.com/images/willy4202/post/ddb9608e-8d5c-42bd-a0dc-fc4b44383075/image.gif)

- 회원가입

```
   - 필수 입력 사항: 이름, 아이디, 이메일, 비밀번호, 비밀번호 확인
   - 유효성 검사 완료 시, 회원가입 버튼 활성화
   - 인풋 창 클릭시 유효성 검사 문구 출력
   - 아이디: 중복 확인, `@`, `.`포함 여부 확인
   - 비밀번호: 문자, 특수 문자, 숫자가 각각 1개 이상이면서 총 8자 이상
   - 비밀번호 확인: 비밀번호와 동일해야함
   - 이름 : 2글자 이상시 확인 가능
```

- 로그인

```
- 아이디 및 비밀번호 유효성 검사 후 로그인 버튼 활성화
- 회원정보 일치 여부에 따른 메시지 출력
```

![](https://velog.velcdn.com/images/willy4202/post/56dff6da-9575-407c-a1f5-b76a28115983/image.gif)

- 메인 페이지

```
- 캐러셀 구현
- 반응형 배너 구현
- Z-index 활용한, 클릭 범위 제한 및 레이아웃 구성
- path, query parameter 활용한 동적 페이지 구현
```

![](https://velog.velcdn.com/images/willy4202/post/8231c0b4-0747-411e-9550-bba4debf6c60/image.gif)

- 상품 리스트

```
- 카테고리 선택에 따른 맞춤 상품 리스트 정렬
- 배열 형태로 정렬되어진 상품 구조
- 페이지네이션 구현
- 상품 정보에 따른 정렬 기능 추가 (인기순, 가격순 등)
```

![](https://velog.velcdn.com/images/willy4202/post/5aebed4e-3424-4e37-9b96-30085d2d778b/image.gif)

- 상품 상세보기

```
- 상품 별점 반영 가능한 댓글 창 구현
- 사이즈, 수량, 컬러 선택 후 장바구니 버튼 클릭 시 백엔드 서버로 유저 데이터 전송
- path Parameter 적용해서, 각기 다른 상품 정보를 받아올 수 있는 기능 구현
- 할인율 반영 가능
- 재고, 주문 수량이 0 이하로 내려갈 시, alert 창 출력
```

![](https://velog.velcdn.com/images/willy4202/post/61dc38a4-7689-4859-b2a7-d93c228bb0d6/image.gif)
![](https://velog.velcdn.com/images/willy4202/post/7a35bd19-637f-4cdf-a071-fdb00abec79f/image.gif)

- 장바구니

```
- 토큰 반영 후, 서로 다른 장바구니 리스트 출력 가능
- 상품이 존재하지 않는 화면
- 상품 전체 삭제 가능
- 재고, 주문 수량이 0 이하로 내려갈 시, alert창 출력
```

![](https://velog.velcdn.com/images/willy4202/post/06b90a6d-c295-44d2-ade2-bc287b54bd9f/image.gif)

- 푸터

```
- 상세 정보 모달 창 구현
```

![](blob:https://velog.io/f68139d1-902c-4bd2-bf48-728188e17e95)

### Reference

이 프로젝트는 `라인 프렌즈 스토어` 사이트를 참조하여 학습목적으로 만들었습니다.
실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.

## ERD 
![Untitled](https://user-images.githubusercontent.com/95554757/167082163-f9e4ce7b-d72c-4a83-822c-0e43d8c9c2f0.png)

## API
- Postman
https://documenter.getpostman.com/view/20639142/UyxbsVsX

## 구현기능

### Users

- 회원가입
- 로그인

### Products

- Topic View : Topic과 해당되는 Product를 반환
  - Product List View : 
  - filtering
  - search
  - sort
  - offset limit
- Product Detail View
  - path parameter를 이용한 product 식별
  - identification_decorator를 사용한 user 정보 반환    
  
- Review View:
  login decorator 를 사용한 

### Payments

- Cart View:

### Core

- Login Decorator