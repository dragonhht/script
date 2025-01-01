#!/usr/bin/env bash

# docker安装
install() {
  cd $(dirname $0)
  RUN_HOME=$(pwd)
  # 解压目录
  temp_dir=$RUN_HOME/temp_dir

  # 创建文件夹
  [ -d ${temp_dir} ] || mkdir -p $temp_dir

  # 安装docker
  tar -xvf $RUN_HOME/installer/docker-27.4.1.tgz -C $temp_dir && chmod 755 -R $temp_dir/docker && cp $temp_dir/docker/* /usr/bin/
  # 清理解压后的文件
  rm -rf $temp_dir

  # 配置docker服务
  tee /etc/systemd/system/docker.service <<-'EOF'
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID

TimeoutSec=0

RestartSec=2

ExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT
Restart=always

TimeoutStartSec=0


LimitNOFILE=infinity
LimitNPROC=infinity

LimitCORE=infinity

Delegate=yes
KillMode=process
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
EOF

  chmod +x /etc/systemd/system/docker.service

  echo '创建docker工作目录并创建daemon.json配置文件...'
  mkdir -p /etc/docker && mkdir -p /opt/app/dockerWork
  tee /etc/docker/daemon.json <<-'EOF'
{
        "data-root":"/opt/app/dockerWork",
        "registry-mirrors": ["https://registry.docker-cn.com","http://hub-mirror.c.163.com","https://hub.littlediary.cn","https://docker.unsee.tech"]
}
EOF

  systemctl daemon-reload
  systemctl enable docker.service
  systemctl start docker

  docker -v
  if [ $? -eq 0 ]; then
    echo "docker 安装成功"
  else
    echo "docker 安装失败"
    exit 1
  fi

}

# 卸载docker
uninstall() {
  echo "停止所有容器服务"
  docker stop $(docker ps -a -q)
  echo "删除所有容器"
  docker rm $(docker ps -a -q)
  echo "删除docker所有镜像"
  docker rmi -f $(docker images -q)
  echo '停止docker服务...'
  systemctl stop docker
  echo '取消开机自启...'
  systemctl disable docker
  echo '删除docker相关包...'
  cd /usr/bin/ && rm -rf containerd* ctr docker* dockerd runc
  echo '取消docker.service注册文件...'
  cd /etc/systemd/system/ && rm -rf docker.service
  echo '删除docker配置文件...'
  cd /etc/ && rm -rf docker/* && rm -rf /data/app/dockerWork
  echo 'yum方式清空docker配置文件...'
  yum remove -y docker-ce docker-ce-cli containerd.io
  rm -rf /var/lib/docker && rm -rf /var/lib/containerd
  echo '重新加载配置文件...'
  systemctl daemon-reload
  echo 'docker卸载成功！！！'
}

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
