FROM python:3.9-slim-bookworm

# 设置环境变量，接受微软的协议
ENV ACCEPT_EULA=Y

# 安装基础依赖
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++ \
    curl \
    gnupg \
    && apt-get clean

# 添加微软仓库（针对 ARM64 架构的 Debian 12）
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg \
    && echo "deb [arch=arm64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list

# 安装 ODBC 18 驱动
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc

WORKDIR /app
COPY . .

# 安装 Python 库
RUN pip install --no-cache-dir flask pyodbc

CMD ["python", "app.py"]