import os
import sys
import json
import shutil
import threading
import subprocess
from pathlib import Path


class MinecraftInstaller:
    def __init__(self, install_path):
        self.install_path = Path(install_path)
        self.versions_path = self.install_path / 'versions'
        self.libraries_path = self.install_path / 'libraries'
        os.makedirs(self.versions_path, exist_ok=True)
        os.makedirs(self.libraries_path, exist_ok=True)

    def install(self, mc_jar_path, forge_jar_path, version_json_path):
        """安装MC本体和Forge到指定路径"""
        # 读取版本信息
        with open(version_json_path, 'r') as f:
            version_data = json.load(f)

        version_id = version_data['id']
        version_dir = self.versions_path / version_id
        os.makedirs(version_dir, exist_ok=True)

        # 安装MC本体
        mc_dest = version_dir / f'{version_id}.jar'
        shutil.copy(mc_jar_path, mc_dest)
        print(f"已安装MC本体: {mc_dest}")

        # 安装Forge
        forge_dest = version_dir / f'{version_id}-forge.jar'
        shutil.copy(forge_jar_path, forge_dest)
        print(f"已安装Forge: {forge_dest}")

        # 保存版本JSON
        json_dest = version_dir / f'{version_id}.json'
        shutil.copy(version_json_path, json_dest)
        print(f"已保存版本配置: {json_dest}")

        return version_id


class MinecraftLauncher:
    def __init__(self, install_path, username='irmaker'):
        self.install_path = Path(install_path)
        self.username = username
        self.versions_path = self.install_path / 'versions'

    def _get_version_id(self):
        """获取安装目录下的唯一版本ID"""
        versions = [d for d in os.listdir(self.versions_path)
                    if os.path.isdir(self.versions_path / d)]

        if len(versions) != 1:
            raise RuntimeError("安装目录必须包含且仅包含一个MC版本")
        return versions[0]

    def _calculate_memory(self):
        """自动计算最大可用内存（保留1GB给系统）"""
        if sys.platform == 'win32':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            mem = kernel32.GetPhysicallyInstalledSystemMemory()
            total_mb = mem // 1024 // 1024
        elif sys.platform == 'darwin':
            import subprocess
            mem = subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip()
            total_mb = int(mem) // 1024 // 1024
        else:  # Linux
            with open('/proc/meminfo') as f:
                mem = f.readline().split()[1]
                total_mb = int(mem) // 1024

        return f"{max(total_mb - 1024, 4096)}M"  # 至少4GB

    def launch(self):
        """启动Minecraft游戏"""
        version_id = self._get_version_id()
        version_dir = self.versions_path / version_id
        json_file = version_dir / f'{version_id}.json'

        with open(json_file, 'r') as f:
            version_data = json.load(f)

        # 准备启动命令
        jar_path = version_dir / f'{version_id}.jar'
        memory = self._calculate_memory()

        cmd = [
            'java',
            f'-Xmx{memory}',  # 最大内存
            f'-Xms{memory}',  # 初始内存
            '-jar',
            str(jar_path),
            '--username', self.username,
            '--gameDir', str(self.install_path),
            '--assetsDir', str(self.install_path / 'assets'),
            '--assetIndex', version_data.get('assetIndex', '1.16'),
            '--version', version_id
        ]

        # 添加Forge支持
        if 'forge' in version_id.lower():
            cmd.extend(['--launchTarget', 'fmlclient'])

        print("启动命令:", ' '.join(cmd))

        # 在新线程中启动游戏
        def run_game():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )

                # 实时打印输出
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())

            except Exception as e:
                print(f"启动失败: {str(e)}")

        thread = threading.Thread(target=run_game, daemon=True)
        thread.start()
        print("游戏已在后台线程启动...")
        return thread
