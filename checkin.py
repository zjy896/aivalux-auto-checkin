#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AIvalux 自动签到脚本
每日自动登录并完成签到任务
"""

import os
import sys
import time
import json
import requests
from datetime import datetime


class AIvaluxCheckin:
    """AIvalux签到类"""

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.base_url = "https://www.aivalux.com"
        self.session = requests.Session()
        self.access_token = None

        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Origin': self.base_url,
        })

    def log(self, message, level="INFO"):
        """日志输出"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def login(self):
        """登录获取access_token"""
        login_url = f"{self.base_url}/api/v1/auth/login"

        payload = {
            "email": self.email,
            "password": self.password
        }

        try:
            self.log("开始登录...")
            response = self.session.post(
                login_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    self.access_token = data['data']['access_token']
                    user_info = data['data']['user']
                    self.log(f"登录成功！用户: {user_info['email']}, 余额: {user_info['balance']}")
                    return True
                else:
                    self.log(f"登录失败: {data.get('message')}", "ERROR")
                    return False
            else:
                self.log(f"登录请求失败: HTTP {response.status_code}", "ERROR")
                return False

        except Exception as e:
            self.log(f"登录异常: {str(e)}", "ERROR")
            return False

    def check_status(self):
        """检查签到状态"""
        status_url = f"{self.base_url}/qiandao/api/status"

        if not self.access_token:
            self.log("未登录，无法检查状态", "ERROR")
            return None

        try:
            response = self.session.get(
                status_url,
                headers={'Authorization': f'Bearer {self.access_token}'}
            )

            if response.status_code == 200:
                data = response.json()
                self.log(f"签到状态: {json.dumps(data, ensure_ascii=False)}")
                return data
            else:
                self.log(f"获取状态失败: HTTP {response.status_code}", "ERROR")
                return None

        except Exception as e:
            self.log(f"检查状态异常: {str(e)}", "ERROR")
            return None

    def checkin(self):
        """执行签到"""
        checkin_url = f"{self.base_url}/qiandao/api/checkin"

        if not self.access_token:
            self.log("未登录，无法签到", "ERROR")
            return False

        try:
            self.log("开始签到...")
            response = self.session.post(
                checkin_url,
                json={},  # 发送空的JSON对象
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )

            if response.status_code == 200:
                data = response.json()
                self.log(f"签到响应: {json.dumps(data, ensure_ascii=False)}")

                # 根据响应判断是否成功
                if data.get('ok'):
                    self.log("✅ 签到成功！", "SUCCESS")
                    return True
                else:
                    self.log(f"签到返回: {data}", "INFO")
                    return False
            elif response.status_code == 400:
                # 可能已经签到过了
                try:
                    data = response.json()
                    if 'already' in str(data).lower() or '已签到' in str(data):
                        self.log("ℹ️ 今日已签到", "INFO")
                        return True
                except:
                    pass
                self.log(f"签到失败: {response.text}", "ERROR")
                return False
            else:
                self.log(f"签到请求失败: HTTP {response.status_code} - {response.text}", "ERROR")
                return False

        except Exception as e:
            self.log(f"签到异常: {str(e)}", "ERROR")
            return False

    def run(self):
        """执行完整的签到流程"""
        self.log("=" * 50)
        self.log("AIvalux 自动签到脚本启动")
        self.log("=" * 50)

        # 步骤1: 登录
        if not self.login():
            self.log("登录失败，退出程序", "ERROR")
            return False

        time.sleep(1)

        # 步骤2: 检查状态
        status = self.check_status()

        # 检查今天是否已经签到
        if status and status.get('ok') and status.get('data', {}).get('today', {}).get('checked_in'):
            self.log("✅ 今日已签到，无需重复签到", "SUCCESS")
            self.log("=" * 50)
            return True

        time.sleep(1)

        # 步骤3: 执行签到
        success = self.checkin()

        self.log("=" * 50)
        if success:
            self.log("签到流程完成 ✅", "SUCCESS")
        else:
            self.log("签到流程失败 ❌", "ERROR")
        self.log("=" * 50)

        return success


def main():
    """主函数"""
    # 从环境变量获取账号密码
    email = os.getenv('AIVALUX_EMAIL')
    password = os.getenv('AIVALUX_PASSWORD')

    if not email or not password:
        print("错误: 请设置环境变量 AIVALUX_EMAIL 和 AIVALUX_PASSWORD")
        print("示例: export AIVALUX_EMAIL='your@email.com'")
        print("      export AIVALUX_PASSWORD='yourpassword'")
        sys.exit(1)

    # 创建签到实例并运行
    checkin = AIvaluxCheckin(email, password)
    success = checkin.run()

    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
