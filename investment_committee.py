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
             
        # 2. Load Personas
        self.personas = {}
        self.lessons = "" # Memory Bank
        self._load_personas()
        self._load_lessons()

    def _load_lessons(self):
        """Load past lessons/principles."""
        path = os.path.join(KNOWLEDGE_DIR, "lessons.md")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.lessons = f.read()
            print("🧠 Memory Loaded: lessons.md (Principles & Past Mistakes)")
        else:
            print("⚠️ Memory Empty: No lessons.md found.")

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
        
        scores = {}
        verdicts = {}

        for p in targets:
            system_prompt = self.personas[p]
            
            # Inject Past Lessons (The "Learning" Mechanism)
            if self.lessons:
                system_prompt += f"\n\n### 🧠 MEMORY & PRINCIPLES (FROM PAST TRADES):\n{self.lessons}\n\n(IMPORTANT: Use these principles to guide your current analysis. Do not repeat past mistakes.)"

            # Add instruction for structured output (Score & Verdict)
            structured_instruction = """
IMPORTANT: 
1. Please output your analysis in **CHINESE (Simplified)**.
2. At the end of your analysis, you MUST provide a structured summary in exactly this format:
---
SCORE: [0-10]
VERDICT: [YES/NO/WATCH]
REASON: [One short sentence in Chinese]
---
"""
            
            print(f"\n👤 Consulting {p.upper()}...")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt + structured_instruction},
                        {"role": "user", "content": f"Please analyze this trade idea:\n{trade_idea}"}
                    ],
                    temperature=0.7
                )
                
                analysis = response.choices[0].message.content
                print("-" * 40)
                print(analysis)
                print("-" * 40)
                
                # Extract score and verdict
                match_score = re.search(r'SCORE:\s*(\d+(\.\d+)?)', analysis)
                match_verdict = re.search(r'VERDICT:\s*(YES|NO|WATCH)', analysis, re.IGNORECASE)
                
                if match_score:
                    scores[p] = float(match_score.group(1))
                if match_verdict:
                    verdicts[p] = match_verdict.group(1).upper()
                
                report_content += f"## {p.capitalize()} 视角\n\n{analysis}\n\n---\n\n"
                
            except Exception as e:
                error_msg = f"❌ Error consulting {p}: {e}"
                print(error_msg)
                report_content += f"## {p.capitalize()} 视角\n\n{error_msg}\n\n"

        print("\n" + "="*60)
        
        # Calculate Final Score
        if scores:
            avg_score = sum(scores.values()) / len(scores)
            
            # Weighted Consensus Logic
            # If Taleb says NO (Score < 3), the whole deal might be killed (Veto power on ruin risk)
            taleb_score = scores.get('taleb', 10)
            if taleb_score < 3:
                final_verdict = "VETOED (Risk of Ruin)"
                avg_score = min(avg_score, taleb_score) # Cap score at Taleb's level
            elif avg_score >= 7.5:
                final_verdict = "STRONG BUY (强力推荐)"
            elif avg_score >= 6.0:
                final_verdict = "BUY / ACCUMULATE (买入/积累)"
            elif avg_score >= 4.0:
                final_verdict = "HOLD / WATCH (持有/观察)"
            else:
                final_verdict = "SELL / AVOID (卖出/回避)"
                
            summary = f"""
## 🏁 投资委员会最终决议 (FINAL VERDICT)

**综合评分**: {avg_score:.1f} / 10
**决策建议**: {final_verdict}

### 投票明细:
"""
            for p in targets:
                s = scores.get(p, "N/A")
                v = verdicts.get(p, "N/A")
                summary += f"- **{p.capitalize()}**: {s}/10 ({v})\n"
            
            print(summary)
            report_content = summary + "\n---\n" + report_content
            
        print("🏁 Committee Session Adjourned.")
        
        # Save report
        filename = f"report_{trade_idea[:20].replace(' ', '_').replace('/', '-')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"📄 Report saved to: {filename}")

    def update_principles(self, trade_name: str, outcome: str, lessons_learned: str):
        """
        Auto-update the lessons.md file with new principles.
        """
        path = os.path.join(KNOWLEDGE_DIR, "lessons.md")
        
        # Structure the new entry
        new_entry = f"""
## 交易复盘: {trade_name}
- **结果**: {outcome}
- **教训**: {lessons_learned}
- **新原则**: [自动生成] 当 {lessons_learned.split(' ')[0]} 发生时，总是检查...
"""
        
        # In a real agent, we would use an LLM to refine the principle.
        # For now, let's append it directly or use LLM to format it.
        
        prompt = f"""
        请根据以下交易复盘结果，提炼一条简洁、可执行的“硬性规则”或“投资原则”（使用中文Markdown格式）：
        
        交易名称: {trade_name}
        结果: {outcome}
        教训: {lessons_learned}
        
        请只输出原则内容，不要包含其他废话。
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            refined_principle = response.choices[0].message.content.strip()
            
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\n\n{refined_principle}")
            
            print(f"🧠 Principles Updated in {path}")
            # Reload memory
            self._load_lessons() # Fixed indentation here
            
        except Exception as e:
            print(f"❌ Failed to update principles: {e}")

def main():
    print("""
#######################################################
#   🏛️  INVESTMENT COMMITTEE AGENT (5-EYES)  🏛️   #
#                                                     #
#   1. Analyze Trade (Type your idea)                 #
#   2. Add Lesson (Type 'learn: [Trade] [Result]...') #
#######################################################
    """)
    
    agent = InvestmentCommitteeAgent()
    
    if not agent.personas:
        print("❌ No personas loaded. Please check the 'knowledge' directory.")
        return

    while True:
        try:
            user_input = input("\n> Enter Command (or 'exit'): ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            if not user_input.strip():
                continue
                
            # Check for "learn:" command
            if user_input.lower().startswith("learn:"):
                # Expected format: learn: Tesla Short, Lost 20%, Don't fight trend
                try:
                    parts = user_input[6:].split(',')
                    if len(parts) >= 2:
                        trade = parts[0].strip()
                        outcome = parts[1].strip()
                        lesson = ",".join(parts[2:]).strip() if len(parts) > 2 else "General Observation"
                        agent.update_principles(trade, outcome, lesson)
                    else:
                        print("⚠️ Usage: learn: [Trade Name], [Outcome], [Lesson Learned]")
                except Exception as e:
                     print(f"⚠️ Error parsing learn command: {e}")
            else:
                # Default to analyze
                agent.analyze(user_input)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
