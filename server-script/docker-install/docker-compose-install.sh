#!/usr/bin/env bash

# 安装
install() {
  cd $(dirname $0)
  RUN_HOME=$(pwd)

  cp -f $RUN_HOME/installer/docker-compose-linux-x86_64 /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
  docker-compose -v
  if [ $? -eq 0 ]; then
    echo "docker-compose 安装成功"
  else
    echo "docker-compose 安装失败"
    exit 1
  fi
}

# 卸载
uninstall() {
  echo '删除docker-compose...'
  rm -rf /usr/local/bin/docker-compose
  echo 'docker-compose卸载成功！！！'
}

# 说明
usage() {
  echo "Usage: sh $0 [install|uninstall]"
  exit 1
}

case "$1" in
"install")
  install
  ;;
"uninstall")
  uninstall
  ;;
*)
  usage
  ;;
esac

exit 0
