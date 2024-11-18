FROM gitpod/workspace-full:2024-11-15-13-22-52

# Python環境のセットアップ
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# AWS CLIのインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "aws-cli.zip" && \
  unzip aws-cli.zip -d aws-cli && \
  sudo ./aws-cli/install && \

# AWS SAM CLIのインストール
RUN curl "https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip" -o "aws-sam-cli.zip" && \
  unzip aws-sam-cli.zip -d aws-sam-cli && \
  sudo ./aws-sam-cli/install && \
