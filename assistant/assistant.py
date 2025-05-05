from openai import OpenAI
import tiktoken
from .config import API_KEY, MODEL, SYS_PROMPT_WATER_CEM_CONC, SYS_PROMPT_JSON_OUT, FEEDBACK_LOG
from .models import Response_w_c_conc, AssistantType
from .pdf_utils import extract_pdf_text, split_text
from .logger import logger

class LabAssistant:
    def __init__(self, assistant_type: AssistantType):
        self.client = OpenAI(api_key=API_KEY)
        self.assistant_type = assistant_type
        self.sys_prompt = self.get_sys_prompt()
        self.response_format = self.get_response_format()
        self.assistant_id = self._load_or_create_assistant()

    def get_response_format(self):
        if self.assistant_type == AssistantType.WaterCementJson:
            return {"type": "json_schema", "json_schema": Response_w_c_conc.schema()}
        return None

    def get_sys_prompt(self):
        if self.assistant_type == AssistantType.WaterCementConc:
            return SYS_PROMPT_WATER_CEM_CONC
        elif self.assistant_type == AssistantType.WaterCementJson:
            return SYS_PROMPT_JSON_OUT
        elif self.assistant_type == AssistantType.AdditiveConc:
            return SYS_PROMPT_WATER_CEM_CONC
        return "You are a helpful assistant."

    def _load_or_create_assistant(self):
        try:
            assistant = self.client.beta.assistants.create(
                name="Lab Assistant V1",
                instructions=self.sys_prompt,
                model=MODEL,
                response_format=self.response_format
            )
            logger.info(f"Created assistant: {assistant.id}")
            return assistant.id
        except Exception as e:
            logger.error(f"Failed to create assistant: {e}")
            raise

    def load_or_create_thread(self, file_path):
        thread = self.create_thread()
        content = extract_pdf_text(file_path)
        chunks = split_text(content)
        for chunk in chunks:
            self.add_message_to_thread(thread.id, chunk)
        return thread.id

    def upload_file(self, file_path):
        try:
            file = self.client.files.create(
                file=open(file_path, "rb"),
                purpose='assistants'
            )
            return file
        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            raise

    def create_thread(self):
        try:
            thread = self.client.beta.threads.create()
            logger.info(f"Created thread: {thread.id}")
            return thread
        except Exception as e:
            logger.error(f"Failed to create thread: {e}")
            raise

    def add_message_to_thread(self, thread_id, message_content):
        try:
            return self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message_content
            )
        except Exception as e:
            logger.error(f"Failed to add message to thread {thread_id}: {e}")
            raise

    def run_thread(self, thread_id):
        try:
            return self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
                response_format=self.response_format
            )
        except Exception as e:
            logger.error(f"Failed to run thread {thread_id}: {e}")
            raise

    def get_run_output(self, thread_id):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )
        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            message = messages.data[0]
            text = message.content[0].text.value
            message_id = message.id
            return text, message_id
        else:
            return None, None

    @staticmethod
    def get_token_count(text):
        encoding = tiktoken.encoding_for_model(MODEL)
        return len(encoding.encode(text))

