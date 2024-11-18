FROM gitpod/workspace-full:2024-11-15-13-22-52

# Python環境のセットアップ
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# AWS CLIのインストール
RUN curl -fSsl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "aws-cli.zip" && \
  unzip aws-cli.zip && \
  sudo ./aws/install && \
  rm aws-cli.zip

# AWS SAM CLIのインストール
RUN curl -fSsl "https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip" -o "aws-sam-cli.zip" && \
  unzip aws-sam-cli.zip && \
  sudo ./aws-sam-cli-linux-x86_64/install && \
  rm aws-sam-cli.zip
