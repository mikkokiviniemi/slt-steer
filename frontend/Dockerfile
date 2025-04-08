FROM node:23-slim as build

COPY . .

RUN npm install

RUN npm run build

# typecheck
RUN npm run lint 

CMD ["npm", "run", "serve"]