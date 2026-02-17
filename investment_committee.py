import os
import sys
import re
from typing import Dict, List, Optional
try:
    from openai import OpenAI
    import httpx
except ImportError:
    print("Error: 'openai' or 'httpx' library not found. Please run: pip install openai httpx")
    sys.exit(1)

# Default paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")

class InvestmentCommitteeAgent:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Investment Committee Agent.
        """
        # 1. Setup API Key and Base URL
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("ARK_API_KEY") or os.environ.get("VOLCENGINE_API_KEY")
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL") or os.environ.get("ARK_BASE_URL")
        if (not self.base_url) and os.environ.get("ARK_API_KEY"):
            self.base_url = "https://ark.cn-beijing.volces.com/api/v3"
        
        # Set default model based on provider or env var
        self.model = model or os.environ.get("OPENAI_MODEL_NAME") or "gpt-4o"
        
        # Special handling for Ollama (needs 'ollama' as fake key if not set)
        if self.base_url and "localhost" in self.base_url and not self.api_key:
            self.api_key = "ollama"

        # Special handling for Gemini:
        # The official OpenAI SDK appends /chat/completions to base_url if it's not present.
        # But Google's endpoint structure is: https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
        # If we set base_url=".../v1beta/openai/", SDK adds ".../v1beta/openai/chat/completions" (correct).
        # However, the error "models/gemini-1.5-flash is not found" suggests it might be hitting the wrong endpoint or model name.
        
        if "generativelanguage.googleapis.com" in (self.base_url or ""):
             # Try forcing the standard OpenAI-compatible endpoint
             if "openai" not in self.base_url:
                 self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
             print("⚠️ Using Gemini endpoint: " + self.base_url)
        
        if not self.api_key:
             print("⚠️ Warning: OPENAI_API_KEY not found. Some providers might require it.", file=sys.stderr)

        # 2. Initialize OpenAI Client with Robustness Settings
        try:
            verify_env = (os.environ.get("OPENAI_HTTP_VERIFY") or "true").strip().lower()
            verify = verify_env not in {"0", "false", "no"}
            http_client = httpx.Client(verify=verify, timeout=60.0)
        except Exception as e:
            print(f"⚠️ Warning: Could not create custom httpx client: {e}")
            http_client = None

        try:
            self.client = OpenAI(
                api_key=self.api_key, 
                base_url=self.base_url,
                http_client=http_client
            )
            print(f"🔌 Connected to: {self.base_url or 'OpenAI Official'}")
            print(f"🤖 Using Model: {self.model}")
        except Exception as e:
             print(f"❌ Error initializing OpenAI client: {e}")
             sys.exit(1)
             
        # 3. Load Personas
        self.personas = {}
        self._load_personas()

    def _load_personas(self):
        """Load system prompts from knowledge files."""
        files = {
            "buffett": "buffett.md",
            "lynch": "lynch.md",
            "soros": "soros.md",
            "marks": "marks.md",
            "taleb": "taleb.md"
        }
        
        print(f"📚 Loading investment philosophies from {KNOWLEDGE_DIR}...")
        
        for key, filename in files.items():
            path = os.path.join(KNOWLEDGE_DIR, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Strip frontmatter (--- ... ---)
                    # Simple regex to remove the first YAML block
                    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                    self.personas[key] = content.strip()
                print(f"  ✅ Loaded {key.capitalize()}")
            else:
                print(f"  ❌ Warning: Could not find {filename}")

    def analyze(self, trade_idea: str, persona: str = "all") -> None:
        """
        Analyze a trade idea using one or all personas.
        """
        if persona == "all":
            targets = self.personas.keys()
        elif persona in self.personas:
            targets = [persona]
        else:
            print(f"❌ Unknown persona: {persona}")
            return

        print(f"\n🔍 Analyzing Trade Idea: '{trade_idea}'\n")
        print("="*60)
        
        report_content = f"# Investment Committee Report: {trade_idea}\n\n"

        for p in targets:
            system_prompt = self.personas[p]
            
            # Add specific instruction to be concise for the committee report
            # The original prompts are quite detailed, which is good.
            
            print(f"\n👤 Consulting {p.upper()}...")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Please analyze this trade idea:\n{trade_idea}"}
                    ],
                    temperature=0.7
                )
                
                analysis = response.choices[0].message.content
                print("-" * 40)
                print(analysis)
                print("-" * 40)
                
                report_content += f"## {p.capitalize()}'s Perspective\n\n{analysis}\n\n---\n\n"
                
            except Exception as e:
                error_msg = f"❌ Error consulting {p}: {e}"
                print(error_msg)
                report_content += f"## {p.capitalize()}'s Perspective\n\n{error_msg}\n\n"

        print("\n" + "="*60)
        print("🏁 Committee Session Adjourned.")
        
        # Save report
        filename = f"report_{trade_idea[:20].replace(' ', '_')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"📄 Report saved to: {filename}")

def main():
    print("""
#######################################################
#   🏛️  INVESTMENT COMMITTEE AGENT (5-EYES)  🏛️   #
#                                                     #
#   1. Buffett (Value & Moat)                         #
#   2. Lynch (Growth & PEG)                           #
#   3. Soros (Reflexivity & False Narratives)         #
#   4. Marks (Cycles & Risk First)                    #
#   5. Taleb (Tail Risk & Convexity)                  #
#######################################################
    """)
    
    agent = InvestmentCommitteeAgent()
    
    if not agent.personas:
        print("❌ No personas loaded. Please check the 'knowledge' directory.")
        return

    while True:
        try:
            user_input = input("\n> Enter Trade Idea (or 'exit'): ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            if not user_input.strip():
                continue
                
            agent.analyze(user_input)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
