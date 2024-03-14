from openai import OpenAI
import agentops
from agentops import record_function
from packaging.version import parse
from importlib import import_module
import sys


ao_client = agentops.Client()

api = 'openai'
if api in sys.modules:
    module = import_module(api)
    if api == 'openai':
        if hasattr(module, '__version__'):
            module_version = parse(module.__version__)
            print('openai version: ', module_version)


@record_function('sample function being recorded')
def call_openai():
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with a piece of code, and your task is to explain it in a concise way."
            },
            {
                "role": "user",
                "content": "class Log:\n        def __init__(self, path):\n            dirname = os.path.dirname(path)\n            os.makedirs(dirname, exist_ok=True)\n            f = open(path, \"a+\")\n    \n            # Check that the file is newline-terminated\n            size = os.path.getsize(path)\n            if size > 0:\n                f.seek(size - 1)\n                end = f.read(1)\n                if end != \"\\n\":\n                    f.write(\"\\n\")\n            self.f = f\n            self.path = path\n    \n        def log(self, event):\n            event[\"_event_id\"] = str(uuid.uuid4())\n            json.dump(event, self.f)\n            self.f.write(\"\\n\")\n    \n        def state(self):\n            state = {\"complete\": set(), \"last\": None}\n            for line in open(self.path):\n                event = json.loads(line)\n                if event[\"type\"] == \"submit\" and event[\"success\"]:\n                    state[\"complete\"].add(event[\"id\"])\n                    state[\"last\"] = event\n            return state"
            }
        ],
        temperature=0.7,
        max_tokens=64,
        top_p=1
    )

    print(response)
    raise ValueError("This is an intentional error for testing.")


call_openai()

ao_client.end_session('Success')
