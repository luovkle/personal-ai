FROM node:18-alpine as node-deps
RUN yarn global add pnpm
WORKDIR /app
COPY ["./package.json", "./pnpm-lock.yaml", "/app/"]
RUN pnpm i --frozen-lockfile

FROM node-deps as node-builder
WORKDIR /app
COPY --from=node-deps ["/app/node_modules", "/app/node_modules/"]
COPY ["./package.json", "./tailwind.config.js", "/app/"]
ADD ["./app/static/input.css", "/app/app/static/"]
ADD ["./app/templates", "/app/app/templates/"]
RUN yarn build:css

FROM python:3.11-alpine as app-deps
RUN pip install pipenv
WORKDIR /app
ENV PIPENV_VENV_IN_PROJECT=1
COPY ["./Pipfile", "./Pipfile.lock", "/app/"]
RUN pipenv install

FROM app-deps as app-runner
WORKDIR /app
COPY --from=node-builder ["/app/app/static/public", "/app/app/static/public/"]
COPY --from=node-builder [ \
  "/app/node_modules/socket.io-client/dist/socket.io.min.js", \
  "/app/app/static/public/socket.io.min.js" \
]
COPY --from=app-deps ["/app/.venv", "/app/.venv/"]
COPY ["./app", "/app/app/"]
EXPOSE 8000
CMD ["pipenv", "run", "prod"]
