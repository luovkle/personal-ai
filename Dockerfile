FROM node:18-alpine as css-deps
RUN yarn global add pnpm
WORKDIR /app
COPY ["./package.json", "./pnpm-lock.yaml", "/app/"]
RUN pnpm i --frozen-lockfile

FROM css-deps as css-builder
WORKDIR /app
COPY --from=css-deps ["/app/node_modules", "/app/node_modules/"]
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
COPY --from=css-builder ["/app/app/static/public", "/app/app/static/public/"]
COPY --from=app-deps ["/app/.venv", "/app/.venv/"]
COPY ["./app", "/app/app/"]
EXPOSE 8000
CMD ["pipenv", "run", "prod"]
