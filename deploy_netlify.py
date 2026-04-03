#!/usr/bin/env python3
"""
Netlify 自动部署脚本
支持本地测试部署和 GitHub Actions 自动部署
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class NetlifyDeploy:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.netlify_config_file = self.script_dir / '.netlify'
        self.netlify_cli = 'netlify'
        
    def check_cli(self):
        """检查 Netlify CLI 是否安装"""
        try:
            result = subprocess.run(
                [self.netlify_cli, '--version'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print(f"✅ Netlify CLI 已安装：{result.stdout.strip()}")
                return True
            else:
                print(f"❌ Netlify CLI 未正常工作")
                return False
        except FileNotFoundError:
            print("❌ Netlify CLI 未安装")
            print("\n安装命令：npm install -g netlify-cli")
            return False
    
    def check_auth(self):
        """检查是否已登录 Netlify"""
        try:
            result = subprocess.run(
                [self.netlify_cli, 'status'],
                capture_output=True, text=True, timeout=10,
                cwd=str(self.script_dir)
            )
            if 'Logged in' in result.stdout:
                print("✅ 已登录 Netlify")
                return True
            else:
                print("⚠️  未登录 Netlify")
                return False
        except Exception as e:
            print(f"❌ 检查登录状态失败：{e}")
            return False
    
    def login(self):
        """登录 Netlify"""
        print("\n🔐 请登录 Netlify...")
        print("方式 1: 使用访问令牌（推荐）")
        print("  1. 访问：https://app.netlify.com/user/applications#personal-access-tokens")
        print("  2. 创建 Personal Access Token")
        print("  3. 运行：netlify login --access-token <YOUR_TOKEN>")
        print("\n方式 2: 浏览器登录")
        print("  运行：netlify login")
        
        # 检查是否有访问令牌环境变量
        access_token = os.environ.get('NETLIFY_AUTH_TOKEN')
        if access_token:
            print(f"\n✅ 发现环境变量 NETLIFY_AUTH_TOKEN")
            try:
                result = subprocess.run(
                    [self.netlify_cli, 'login', '--access-token', access_token],
                    capture_output=True, text=True, timeout=30,
                    cwd=str(self.script_dir)
                )
                if result.returncode == 0:
                    print("✅ 登录成功")
                    return True
                else:
                    print(f"❌ 登录失败：{result.stderr}")
            except Exception as e:
                print(f"❌ 登录异常：{e}")
        
        return False
    
    def init_site(self, site_id=None):
        """初始化站点配置"""
        print("\n🔧 初始化站点配置...")
        
        # 检查是否有 Site ID 环境变量
        if not site_id:
            site_id = os.environ.get('NETLIFY_SITE_ID')
        
        if site_id:
            print(f"✅ 使用环境变量 NETLIFY_SITE_ID: {site_id}")
            # 创建 .netlify 配置文件
            config = {
                'siteId': site_id
            }
            with open(self.netlify_config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ 配置文件已保存：{self.netlify_config_file}")
            return True
        else:
            print("⚠️ 未提供 Site ID，需要手动配置")
            print("\n获取 Site ID 步骤:")
            print("  1. 访问：https://app.netlify.com")
            print("  2. 选择站点 → Site settings")
            print("  3. General → Site details → Site ID")
            print("\n然后设置环境变量：export NETLIFY_SITE_ID=<YOUR_SITE_ID>")
            return False
    
    def deploy(self, prod=False):
        """部署到 Netlify"""
        print("\n🚀 开始部署...")
        
        cmd = [self.netlify_cli, 'deploy']
        
        if prod:
            cmd.append('--prod')
            print("📦 部署到生产环境")
        else:
            print("📦 部署到预览环境")
        
        cmd.extend(['--dir', '.', '--message', 'Auto deploy from GitHub Actions'])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True, text=True, timeout=300,
                cwd=str(self.script_dir)
            )
            
            if result.returncode == 0:
                print("✅ 部署成功！")
                print("\n" + "="*60)
                print(result.stdout)
                print("="*60)
                
                # 提取访问 URL
                for line in result.stdout.split('\n'):
                    if 'Website URL' in line or 'Live URL' in line:
                        print(f"\n🌐 {line.strip()}")
                
                return True
            else:
                print(f"❌ 部署失败：{result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 部署超时（>5 分钟）")
            return False
        except Exception as e:
            print(f"❌ 部署异常：{e}")
            return False
    
    def status(self):
        """显示当前状态"""
        print("\n📊 Netlify 部署状态")
        print("="*60)
        
        # 检查 CLI
        cli_ok = self.check_cli()
        
        # 检查登录
        auth_ok = self.check_auth()
        
        # 检查配置
        config_ok = False
        if self.netlify_config_file.exists():
            with open(self.netlify_config_file) as f:
                config = json.load(f)
                site_id = config.get('siteId', 'N/A')
                print(f"✅ 站点配置：{site_id}")
                config_ok = True
        else:
            print("❌ 站点配置：未初始化")
        
        # 检查环境变量
        env_token = 'NETLIFY_AUTH_TOKEN' in os.environ
        env_site = 'NETLIFY_SITE_ID' in os.environ
        print(f"{'✅' if env_token else '❌'} 环境变量：NETLIFY_AUTH_TOKEN")
        print(f"{'✅' if env_site else '❌'} 环境变量：NETLIFY_SITE_ID")
        
        print("="*60)
        
        if cli_ok and auth_ok and (config_ok or env_site):
            print("✅ 配置完整，可以部署")
            return True
        else:
            print("❌ 配置不完整，需要先配置")
            return False
    
    def run(self, action='status'):
        """运行命令"""
        actions = {
            'status': self.status,
            'login': self.login,
            'init': lambda: self.init_site(),
            'deploy': lambda: self.deploy(prod=True),
            'deploy-preview': lambda: self.deploy(prod=False),
        }
        
        if action in actions:
            return actions[action]()
        else:
            print(f"❌ 未知动作：{action}")
            print("可用动作：status, login, init, deploy, deploy-preview")
            return False


def main():
    import sys
    
    deployer = NetlifyDeploy()
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        action = 'status'
    
    success = deployer.run(action)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
