FROM node:12.2.0-alpine as build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_PATH src/

RUN npm install react-scripts@4.0.3 -g --silent --only=prod

COPY package.json /app/package.json
RUN npm install --only=prod

COPY public/ /app/public
COPY . .
RUN npm run build

FROM node:12.2.0-alpine as publish

WORKDIR /app

RUN npm install serve -g --silent --only=prod

COPY --from=build /app/build build/

CMD ["serve", "-s", "build"]
