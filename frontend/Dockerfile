# Usar imagen oficial de Node.js
FROM node:18-alpine

# Directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Construir la aplicación
RUN npm run build

# Usar servidor Nginx para servir los archivos estáticos
FROM nginx:alpine

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos de build
COPY --from=0 /app/dist /usr/share/nginx/html

# Exponer puerto
EXPOSE 3000

# Comando para ejecutar Nginx
CMD ["nginx", "-g", "daemon off;"]
