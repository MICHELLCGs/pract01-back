# Utiliza la imagen de SDK para compilar el código
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Copia los archivos csproj y restaura las dependencias
COPY *.csproj ./
RUN dotnet restore

# Copia el resto de los archivos del proyecto
COPY . ./

# Compila la aplicación en modo de release
RUN dotnet publish -c Release -o out

# Genera la imagen final con la versión de runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/out .

# Expone el puerto en el que la aplicación se ejecuta
EXPOSE 8080

# Define el comando para ejecutar la aplicación
ENTRYPOINT ["dotnet", "pract04.dll", "--urls", "http://*:8080"]
