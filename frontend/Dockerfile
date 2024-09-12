# 1. Svelte 빌드 과정
FROM node:18 AS builder

WORKDIR /app
COPY ./ /app

RUN npm install
RUN npm run build

# 2. Nginx에 빌드된 파일 배포
FROM nginx:alpine

COPY --from=builder /app/public /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]