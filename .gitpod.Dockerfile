FROM gitpod/workspace-python-3.11:2024-11-20-08-19-55

# Python環境のセットアップ
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# AWS CLIのインストール
RUN curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "aws-cli.zip" && \
  unzip -q aws-cli.zip && \
  sudo ./aws/install && \
  rm aws-cli.zip

# AWS SAM CLIのインストール
RUN curl -sL "https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip" -o "aws-sam-cli.zip" && \
  unzip -q aws-sam-cli.zip -d aws-sam-cli && \
  sudo ./aws-sam-cli/install && \
  rm aws-sam-cli.zip
