# 1. Svelte 빌드 과정
FROM node:18 AS builder

# 작업 디렉터리 설정
WORKDIR /app

# 애플리케이션의 모든 파일 복사
COPY ./ /app

# 패키지 설치 및 빌드
RUN npm install
RUN npm run build

# 2. Nginx를 사용한 정적 파일 제공
FROM nginx:alpine

# 빌드된 Svelte 애플리케이션 복사
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx 설정 파일 복사 (필요 시 커스텀 설정)
COPY nginx.conf /etc/nginx/nginx.conf

# Nginx를 실행
CMD ["nginx", "-g", "daemon off;"]
