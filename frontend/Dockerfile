FROM node:14

WORKDIR /app

COPY . ./

# Install dependencie
RUN npm install

RUN npm run build

EXPOSE 3000

# Start Frontend
CMD ["npm", "start"]