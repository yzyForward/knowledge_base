import sys
import os
from os.path import splitext

from app.core.logger import logger
from app.import_process.agent.state import ImportGraphState, create_default_state
from app.utils.task_utils import add_running_task, add_done_task


def node_entry(state: ImportGraphState) -> ImportGraphState:
    """   一、
    节点: 入口节点 (node_entry)
    为什么叫这个名字: 作为图的 Entry Point，负责接收外部输入并决定流程走向。
    进出节点都要做日志输出【节点+核心参数】
    未来要实现:
    一、进入节点做日志输出【节点+核心参数】
    二、参数校验（local_file_path -> 没有文件传入 -> end;  local_dir -> 没有传入输出文件  -> 创建一个临时的）
    三、主流程：
       1. 接收文件路径local_file_path。
       2. 判断文件类型 (PDF/MD)。
       3. 设置 state 中的路由标记 (is_pdf_read_enabled / is_md_read_enabled)。
       4.从文件名中提取file_title，后续作为元数据
    四、输出节点日志【节点+核心参数】
    """
    # logger.info(f">>> [Stub] 执行节点: {sys._getframe().f_code.co_name}")

# -----------------------------------------------------------------------------------------
    # 一、进入节点做日志输出【节点 + 核心参数】

    # 获取当前函数名
    function_name = sys._getframe().f_code.co_name  # 获取当前函数名
    logger.info(f">>> [{function_name}]开始执行了！现在状态为：{state}")

    # 开始：记录节点运行状态
    add_running_task(state["task_id"], function_name)
# -----------------------------------------------------------------------------------------
    # 二、参数校验，根据文件后缀判断类型

    # 1、进行必要的非空检验
    local_file_path = state["local_file_path"]
    if not local_file_path:
        logger.error(f">>> [{function_name}]参数错误：local_file_path 不能为空！")
        return

    # 2、根据文件后缀判断类型,并且完成state的属性赋值，设置对应解析开关
    if local_file_path.endswith(".md"):
        logger.info(f"【{function_name}】文件类型校验通过：{local_file_path} → MD格式，开启MD解析流程")
        state["is_md_read_enabled"] = True
        state["md_path"] = local_file_path
    elif local_file_path.endswith(".pdf"):
        logger.info(f"【{function_name}】文件类型校验通过：{local_file_path} → PDF格式，开启PDF解析流程")
        state["is_pdf_read_enabled"] = True
        state["pdf_path"] = local_file_path
    else:
        logger.warning(f"【{function_name}】文件类型校验失败：{local_file_path} → 不支持的格式，仅支持.pdf/.md")

    # 3、获取文件标题，作为全局业务标识
    file_name = os.path.basename(local_file_path)
    state["file_title"] = splitext(file_name)[0]
    logger.info(f"【{function_name}】文件标题：{state['file_title']}")

# -----------------------------------------------------------------------------------------
    # 四、结束节点做日志输出【节点+核心参数】
    logger.info(f">>> [{function_name}]节点执行完成！现在状态为：{state}")
    add_done_task(state["task_id"], function_name)
    print(function_name)



    # 模拟简单的路由逻辑，防止报错 (仅 node_entry 需要)
    if "local_file_path" in state:
        path = state["local_file_path"]
        if path.endswith(".pdf"):
            state["is_pdf_read_enabled"] = True
        elif path.endswith(".md"):
            state["is_md_read_enabled"] = True

    return state

if __name__ == '__main__':

    # 单元测试：覆盖不支持类型、MD、PDF三种场景
    logger.info("===== 开始node_entry节点单元测试 =====")

    # 测试1: 不支持的TXT文件
    test_state1 = create_default_state(
        task_id="test_task_001",
        local_file_path="联想海豚用户手册.txt"
    )
    node_entry(test_state1)

    # 测试2: MD文件
    test_state2 = create_default_state(
        task_id="test_task_002",
        local_file_path="小米用户手册.md"
    )
    node_entry(test_state2)

    # 测试3: PDF文件
    test_state3 = create_default_state(
        task_id="test_task_003",
        local_file_path="万用表的使用.pdf"
    )
    node_entry(test_state3)

    logger.info("===== 结束node_entry节点单元测试 =====")















