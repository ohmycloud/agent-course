import os
from openai import OpenAI

class LLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
            base_url=os.environ['OPENAI_BASE_URL']
        )

    def generate_daily_report(self, markdown_content, dry_run=False):
        prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
        if dry_run:
            with open("daily-progress/prompt.txt", "w+") as f:
                f.write(prompt)
            return "DRY RUN"
        print("Before call GPT")

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        print("After call GPT")
        print(response)
        return response.choices[0].message.content
