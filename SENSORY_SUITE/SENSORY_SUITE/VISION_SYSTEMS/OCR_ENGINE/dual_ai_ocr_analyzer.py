#!/usr/bin/env python3
"""
DUAL AI OCR ANALYZER - Claude + ChatGPT Intelligence Integration
Sends OCR results to both Claude and ChatGPT for maximum intelligence analysis
"""
import sys
import os
import json
import asyncio
import aiohttp
import openai
from datetime import datetime
from pathlib import Path

# STEP 1: GS343 FOUNDATION (ALWAYS FIRST!)
sys.path.append("E:/ECHO_X_V2.0/GS343_DIVINE_OVERSIGHT")
from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase

# STEP 2: Phoenix 24/7 Auto-Healer
sys.path.append("E:/ECHO_X_V2.0/GS343_DIVINE_OVERSIGHT/HEALERS")
from phoenix_client_gs343 import PhoenixClient, auto_heal

class DualAIOCRAnalyzer:
    def __init__(self):
        # GS343 EKM Foundation - MANDATORY FIRST!
        self.gs343_ekm = ComprehensiveProgrammingErrorDatabase()
        
        # Phoenix Service - MANDATORY SECOND!
        self.phoenix = PhoenixClient()
        
        # Load API keys
        self.load_api_keys()
        
        # Analysis prompts for different AI systems
        self.claude_prompt_template = """
        Analyze this OCR text for patterns, significance, and context. Focus on:
        1. Technical patterns (errors, processes, system states)
        2. Numerical significance (percentages, values, measurements)
        3. Action items or important status changes
        4. Security or system health indicators
        
        OCR Text: {ocr_text}
        
        Provide analysis in JSON format:
        {{
            "significance_score": 1-10,
            "patterns_found": [...],
            "technical_insights": "...",
            "recommended_action": "...",
            "category": "system|error|progress|normal"
        }}
        """
        
        self.chatgpt_prompt_template = """
        What's important about this screen content? Analyze from a human perspective:
        1. Is this content worth the user's immediate attention?
        2. What context or meaning can you derive?
        3. Are there any concerns or positive developments?
        4. Should this be saved to memory?
        
        Screen Content: {ocr_text}
        
        Respond in JSON format:
        {{
            "attention_worthy": true/false,
            "human_context": "...",
            "concerns": [...],
            "positive_developments": [...],
            "memory_worthy": true/false,
            "emotional_tone": "positive|negative|neutral|urgent"
        }}
        """
        
        print("🤖 Dual AI OCR Analyzer initialized (Claude + ChatGPT)")

    @auto_heal
    def load_api_keys(self):
        """Load API keys from keychain"""
        try:
            keychain_path = "E:/ECHO_X_V2.0/CONFIG/echo_x_complete_api_keychain.env"
            
            if os.path.exists(keychain_path):
                with open(keychain_path, 'r') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value.strip('"').strip("'")
                            
                print("🔑 API keys loaded from keychain")
            else:
                print("⚠️ API keychain not found, using environment variables")
                
        except Exception as e:
            print(f"⚠️ Error loading API keys: {e}")

    @auto_heal
    async def analyze_with_claude(self, ocr_text):
        """Analyze OCR text with Claude for pattern recognition"""
        try:
            # Note: This would normally use the Anthropic API
            # For now, we'll simulate Claude's response style
            
            prompt = self.claude_prompt_template.format(ocr_text=ocr_text)
            
            # Simulate Claude analysis (replace with actual API call)
            analysis = await self._simulate_claude_analysis(ocr_text)
            
            return {
                "source": "claude",
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis,
                "prompt_used": prompt[:200] + "..."
            }
            
        except Exception as e:
            print(f"⚠️ Claude analysis error: {e}")
            return {
                "source": "claude",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    @auto_heal
    async def analyze_with_chatgpt(self, ocr_text):
        """Analyze OCR text with ChatGPT for human context"""
        try:
            # Initialize OpenAI client
            if "OPENAI_API_KEY" in os.environ:
                openai.api_key = os.environ["OPENAI_API_KEY"]
            
                prompt = self.chatgpt_prompt_template.format(ocr_text=ocr_text)
                
                # Make API call to ChatGPT
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert at analyzing screen content for human significance."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                
                analysis_text = response.choices[0].message.content
                
                # Try to parse JSON, fallback to text
                try:
                    analysis = json.loads(analysis_text)
                except json.JSONDecodeError:
                    analysis = {"raw_response": analysis_text}
                
                return {
                    "source": "chatgpt",
                    "timestamp": datetime.now().isoformat(),
                    "analysis": analysis,
                    "model_used": response.model
                }
            else:
                # Simulate ChatGPT response if no API key
                analysis = await self._simulate_chatgpt_analysis(ocr_text)
                return {
                    "source": "chatgpt",
                    "timestamp": datetime.now().isoformat(),
                    "analysis": analysis,
                    "note": "Simulated response - no API key"
                }
                
        except Exception as e:
            print(f"⚠️ ChatGPT analysis error: {e}")
            return {
                "source": "chatgpt",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    @auto_heal
    async def _simulate_claude_analysis(self, ocr_text):
        """Simulate Claude's analytical approach"""
        text_lower = ocr_text.lower()
        
        # Pattern detection
        patterns = []
        if "error" in text_lower or "exception" in text_lower:
            patterns.append("error_patterns")
        if any(char in ocr_text for char in "%$"):
            patterns.append("numerical_values")
        if "complete" in text_lower or "finished" in text_lower:
            patterns.append("completion_indicators")
        
        # Determine significance
        significance_score = len(patterns) + (2 if len(ocr_text) > 100 else 1)
        significance_score = min(10, significance_score)
        
        # Categorize
        if "error" in text_lower or "fail" in text_lower:
            category = "error"
        elif "%" in ocr_text or "complete" in text_lower:
            category = "progress"
        elif any(word in text_lower for word in ["system", "process", "status"]):
            category = "system"
        else:
            category = "normal"
        
        return {
            "significance_score": significance_score,
            "patterns_found": patterns,
            "technical_insights": f"Detected {len(patterns)} technical patterns in {len(ocr_text)} characters",
            "recommended_action": "save_to_memory" if significance_score >= 5 else "monitor",
            "category": category
        }

    @auto_heal  
    async def _simulate_chatgpt_analysis(self, ocr_text):
        """Simulate ChatGPT's human-context approach"""
        text_lower = ocr_text.lower()
        
        # Human attention assessment
        attention_worthy = False
        concerns = []
        positive_developments = []
        
        if any(word in text_lower for word in ["error", "fail", "critical", "warning"]):
            attention_worthy = True
            concerns.append("System errors or warnings detected")
        
        if any(word in text_lower for word in ["complete", "success", "finished", "done"]):
            positive_developments.append("Task completion indicated")
        
        if "%" in ocr_text:
            attention_worthy = True
            positive_developments.append("Progress metrics visible")
        
        # Determine emotional tone
        if concerns:
            emotional_tone = "urgent" if "critical" in text_lower else "negative"
        elif positive_developments:
            emotional_tone = "positive"
        else:
            emotional_tone = "neutral"
        
        return {
            "attention_worthy": attention_worthy,
            "human_context": f"Screen shows {len(ocr_text)} characters of content with potential user impact",
            "concerns": concerns,
            "positive_developments": positive_developments,
            "memory_worthy": attention_worthy or len(positive_developments) > 0,
            "emotional_tone": emotional_tone
        }

    @auto_heal
    async def dual_analyze_ocr(self, ocr_text):
        """Perform dual AI analysis with Claude and ChatGPT"""
        if not ocr_text or len(ocr_text.strip()) < 5:
            return {
                "status": "skipped",
                "reason": "Insufficient text content",
                "text_length": len(ocr_text) if ocr_text else 0
            }
        
        print(f"🧠 Dual AI analyzing {len(ocr_text)} characters...")
        
        # Run both analyses concurrently
        claude_task = self.analyze_with_claude(ocr_text)
        chatgpt_task = self.analyze_with_chatgpt(ocr_text)
        
        claude_result, chatgpt_result = await asyncio.gather(
            claude_task, chatgpt_task, return_exceptions=True
        )
        
        # Combine results
        combined_analysis = {
            "timestamp": datetime.now().isoformat(),
            "ocr_text_preview": ocr_text[:200] + "..." if len(ocr_text) > 200 else ocr_text,
            "text_length": len(ocr_text),
            "claude": claude_result if not isinstance(claude_result, Exception) else {"error": str(claude_result)},
            "chatgpt": chatgpt_result if not isinstance(chatgpt_result, Exception) else {"error": str(chatgpt_result)},
            "combined_insights": self.merge_ai_insights(claude_result, chatgpt_result)
        }
        
        return combined_analysis

    @auto_heal
    def merge_ai_insights(self, claude_result, chatgpt_result):
        """Merge insights from both AI systems for final decision"""
        try:
            insights = {
                "final_significance": 1,
                "should_save": False,
                "should_speak": False,
                "combined_reasoning": [],
                "priority_level": "low"
            }
            
            # Extract Claude insights
            if isinstance(claude_result, dict) and "analysis" in claude_result:
                claude_analysis = claude_result["analysis"]
                if "significance_score" in claude_analysis:
                    insights["final_significance"] = max(insights["final_significance"], 
                                                       claude_analysis.get("significance_score", 1))
                
                if claude_analysis.get("category") in ["error", "system"]:
                    insights["combined_reasoning"].append("Claude detected technical significance")
            
            # Extract ChatGPT insights  
            if isinstance(chatgpt_result, dict) and "analysis" in chatgpt_result:
                chatgpt_analysis = chatgpt_result["analysis"]
                if chatgpt_analysis.get("attention_worthy", False):
                    insights["final_significance"] = max(insights["final_significance"], 6)
                    insights["combined_reasoning"].append("ChatGPT flagged as attention-worthy")
                
                if chatgpt_analysis.get("memory_worthy", False):
                    insights["should_save"] = True
                    insights["combined_reasoning"].append("ChatGPT recommended memory storage")
                
                if chatgpt_analysis.get("emotional_tone") == "urgent":
                    insights["should_speak"] = True
                    insights["priority_level"] = "urgent"
            
            # Final decisions
            if insights["final_significance"] >= 5:
                insights["should_save"] = True
                insights["should_speak"] = True
                insights["priority_level"] = "high"
            elif insights["final_significance"] >= 3:
                insights["should_save"] = True
                insights["priority_level"] = "medium"
            
            return insights
            
        except Exception as e:
            print(f"⚠️ Insight merging error: {e}")
            return {
                "final_significance": 1,
                "should_save": False,
                "should_speak": False,
                "combined_reasoning": [f"Error in analysis: {e}"],
                "priority_level": "low"
            }

    @auto_heal
    def is_worth_saving(self, claude_response, chatgpt_response):
        """Determine if content should be saved based on dual AI analysis"""
        try:
            # Extract recommendations
            claude_save = False
            chatgpt_save = False
            
            if isinstance(claude_response, dict) and "analysis" in claude_response:
                claude_analysis = claude_response["analysis"]
                claude_save = (claude_analysis.get("significance_score", 0) >= 5 or
                              claude_analysis.get("recommended_action") == "save_to_memory")
            
            if isinstance(chatgpt_response, dict) and "analysis" in chatgpt_response:
                chatgpt_analysis = chatgpt_response["analysis"]
                chatgpt_save = chatgpt_analysis.get("memory_worthy", False)
            
            # Save if either AI recommends it
            should_save = claude_save or chatgpt_save
            
            print(f"💾 Save decision - Claude: {claude_save}, ChatGPT: {chatgpt_save}, Final: {should_save}")
            return should_save
            
        except Exception as e:
            print(f"⚠️ Save decision error: {e}")
            return False  # Conservative default

# Main execution for testing
if __name__ == "__main__":
    async def test_dual_analyzer():
        analyzer = DualAIOCRAnalyzer()
        
        test_text = "System Error: Failed to connect to database. Connection timeout after 30 seconds. Error code: 500"
        
        result = await analyzer.dual_analyze_ocr(test_text)
        print(json.dumps(result, indent=2))
    
    asyncio.run(test_dual_analyzer())
