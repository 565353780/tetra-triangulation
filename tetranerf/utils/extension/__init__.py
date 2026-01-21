import sys
import importlib.util
from pathlib import Path

# 尝试导入编译后的扩展模块
try:
    # 首先尝试直接导入（适用于已安装的情况）
    from . import tetranerf_cpp_extension as cpp
except ImportError:
    # 如果直接导入失败，尝试从当前目录查找 .so 文件
    extension_dir = Path(__file__).parent
    so_files = list(extension_dir.glob("tetranerf_cpp_extension*.so"))
    
    if not so_files:
        # 如果在当前目录找不到，尝试查找 .pyd 文件（Windows）
        so_files = list(extension_dir.glob("tetranerf_cpp_extension*.pyd"))
    
    if so_files:
        # 找到 .so 文件，动态加载
        so_path = so_files[0]
        spec = importlib.util.spec_from_file_location("tetranerf_cpp_extension", so_path)
        cpp = importlib.util.module_from_spec(spec)
        sys.modules["tetranerf.utils.extension.tetranerf_cpp_extension"] = cpp
        spec.loader.exec_module(cpp)
    else:
        raise ImportError(
            f"无法找到 tetranerf_cpp_extension 模块。"
            f"请确保已运行 'cmake . && make' 编译扩展，"
            f"并且 .so 文件位于 {extension_dir}"
        )

triangulate = cpp.triangulate