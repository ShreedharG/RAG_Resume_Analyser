# ──────────────────────────────────────────────
# Frontend Dockerfile — Multi-stage build
# Stage 1: Build React/Vite app with Node
# Stage 2: Serve with Nginx (tiny final image)
# ──────────────────────────────────────────────

# ── Stage 1: Build ──────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first (layer cache: only re-install if deps change)
COPY frontend/package*.json ./

RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build production bundle
RUN npm run build

# ── Stage 2: Serve ──────────────────────────
FROM nginx:alpine AS production

# Remove default Nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom Nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from Stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
