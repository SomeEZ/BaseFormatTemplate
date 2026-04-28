from .abc_message_info import ABCMessageInfo


class MessageInfo(ABCMessageInfo):
    def __init__(self, message_id: str, message_seq: int, real_id: int, real_seq: int):
        self._message_id = message_id
        self._message_seq = message_seq
        self._real_id = real_id
        self._real_seq = real_seq
        self._text_content = ""
        self._image_urls = []
        self._forward_count = 0
        self._has_forward = False

    def get_message_id(self) -> str:
        return self._message_id

    def get_message_seq(self) -> int:
        return self._message_seq

    def get_real_id(self) -> int:
        return self._real_id

    def get_real_seq(self) -> int:
        return self._real_seq

    def set_text_content(self, text_content: str):
        self._text_content = text_content.strip()

    def get_text_content(self) -> str:
        return self._text_content or "无"

    def add_image_url(self, url: str):
        if url:
            self._image_urls.append(url)

    def get_image_urls(self) -> list:
        return self._image_urls

    def get_image_count(self) -> int:
        return len(self._image_urls)

    def has_forward_message(self) -> bool:
        return self._has_forward

    def get_forward_count(self) -> int:
        return self._forward_count

    def process_message_chain(self, message_chain: list):
        text_content = ""
        for msg in message_chain:
            class_name = type(msg).__name__.lower()
            if 'forward' in class_name or isinstance(getattr(msg, 'content', None), list):
                text_content += self.process_forward_message(msg)
            elif 'node' in class_name:
                text_content += self.process_node_message(msg)
            else:
                if hasattr(msg, 'text'):
                    text_content += msg.text.strip()
                if hasattr(msg, 'url') and msg.url:
                    self.add_image_url(msg.url)
        self.set_text_content(text_content)

    def process_forward_message(self, msg):
        content = "\n【合并转发消息】\n"
        content_list = getattr(msg, 'content', None)
        if isinstance(content_list, list):
            self._has_forward = True
            self._forward_count = len(content_list)
            for i, node in enumerate(content_list, 1):
                node_result = self.process_node_message(node)
                if node_result:
                    prefix = f"\n── 消息 {i} ──\n"
                    content += prefix + node_result
        return content

    def process_node_message(self, node, depth=1):
        node_content = ""
        indent = "  " * depth
        nickname = getattr(node, 'nickname', '未知')
        user_id = getattr(node, 'user_id', '未知')
        node_content += f"{indent}发送者: {nickname} ({user_id})\n"
        content_list = getattr(node, 'content', None)
        if isinstance(content_list, list):
            for sub_msg in content_list:
                class_name = type(sub_msg).__name__.lower()
                sub_content = getattr(sub_msg, 'content', None)
                if 'node' in class_name or isinstance(sub_content, list):
                    node_content += f"{indent}└── 嵌套消息:\n"
                    node_content += self.process_node_message(sub_msg, depth + 1)
                else:
                    text = getattr(sub_msg, 'text', '')
                    if text:
                        node_content += f"{indent}内容: {text.strip()}\n"
                    url = getattr(sub_msg, 'url', None)
                    if url:
                        self.add_image_url(url)
                        node_content += f"{indent}[图片]\n"
        return node_content
