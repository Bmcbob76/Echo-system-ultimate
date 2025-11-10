#!/usr/bin/env python3
"""
OCR INTELLIGENCE COORDINATOR - Master Coordination System
Coordinates 4-monitor OCR, dual AI analysis, voice responses, and memory integration
"""
import sys
import os
import json
import asyncio
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path

# STEP 1: GS343 FOUNDATION (ALWAYS FIRST!)
sys.path.append("E:/ECHO_X_V2.0/GS343_DIVINE_OVERSIGHT")
from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase

# STEP 2: Phoenix 24/7 Auto-Healer
sys.path.append("E:/ECHO_X_V2.0/GS343_DIVINE_OVERSIGHT/HEALERS")
from phoenix_client_gs343 import PhoenixClient, auto_heal

# Import our OCR components
from four_monitor_ocr_intelligent import FourMonitorOCRIntelligent
from dual_ai_ocr_analyzer import DualAIOCRAnalyzer

class OCRIntelligenceCoordinator:
    def __init__(self):
        # GS343 EKM Foundation - MANDATORY FIRST!
        self.gs343_ekm = ComprehensiveProgrammingErrorDatabase()
        
        # Phoenix Service - MANDATORY SECOND!
        self.phoenix = PhoenixClient()
        
        # Initialize core components
        self.ocr_system = FourMonitorOCRIntelligent()
        self.ai_analyzer = DualAIOCRAnalyzer()
        
        # Master EKM Integration
        self.master_ekm_path = "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/MASTER_EKM"
        self.create_ocr_intelligence_ekms()
        
        # Intelligence coordination settings
        self.auto_scan_interval = 30  # seconds
        self.auto_scan_enabled = False
        self.intelligence_threshold = 5  # minimum significance for voice announcement
        
        # Performance tracking
        self.scan_history = []
        self.intelligence_stats = {
            "total_scans": 0,
            "significant_findings": 0,
            "ai_analyses": 0,
            "voice_announcements": 0,
            "memory_saves": 0
        }
        
        print("🎯 OCR Intelligence Coordinator initialized")
        print("🔄 4-Monitor OCR + Dual AI + Voice + Memory integration ready")

    @auto_heal
    def create_ocr_intelligence_ekms(self):
        """Create Master EKM databases for OCR intelligence"""
        try:
            # Create OCR Intelligence EKM directories
            ocr_ekm_path = Path(self.master_ekm_path) / "OCR_INTELLIGENCE_EKM"
            sensory_ekm_path = Path(self.master_ekm_path) / "SENSORY_EKM"
            
            for path in [ocr_ekm_path, sensory_ekm_path]:
                path.mkdir(parents=True, exist_ok=True)
            
            # OCR AI Decisions Database
            self.create_ocr_ai_decisions_db(ocr_ekm_path / "ocr_ai_decisions.db")
            
            # Screen Importance Database  
            self.create_screen_importance_db(ocr_ekm_path / "screen_importance.db")
            
            # Dual AI Analysis Database
            self.create_dual_ai_analysis_db(ocr_ekm_path / "dual_ai_analysis.db")
            
            # Sensory Intelligence Database
            self.create_sensory_intelligence_db(sensory_ekm_path / "sensory_intelligence.db")
            
            print("💾 Master EKM databases created for OCR intelligence")
            
        except Exception as e:
            print(f"⚠️ EKM creation error: {e}")

    @auto_heal
    def create_ocr_ai_decisions_db(self, db_path):
        """Create database for AI filtering decisions"""
        with sqlite3.connect(db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS ai_decisions (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    scan_id TEXT,
                    monitor_id INTEGER,
                    ocr_text TEXT,
                    claude_decision TEXT,
                    chatgpt_decision TEXT,
                    final_decision TEXT,
                    significance_score INTEGER,
                    should_save BOOLEAN,
                    should_speak BOOLEAN,
                    reasoning TEXT
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_scan_id ON ai_decisions(scan_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_significance ON ai_decisions(significance_score)')

    @auto_heal  
    def create_screen_importance_db(self, db_path):
        """Create database for AI content ranking"""
        with sqlite3.connect(db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS screen_rankings (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    scan_id TEXT,
                    monitor_id INTEGER,
                    content_preview TEXT,
                    importance_level INTEGER,
                    category TEXT,
                    keywords TEXT,
                    ai_confidence REAL,
                    user_attention_needed BOOLEAN
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_importance ON screen_rankings(importance_level)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_category ON screen_rankings(category)')

    @auto_heal
    def create_dual_ai_analysis_db(self, db_path):
        """Create database for Claude + ChatGPT analysis results"""
        with sqlite3.connect(db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS dual_analysis (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    scan_id TEXT,
                    ocr_content TEXT,
                    claude_analysis TEXT,
                    chatgpt_analysis TEXT,
                    combined_insights TEXT,
                    processing_time REAL,
                    analysis_quality TEXT
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_scan_dual ON dual_analysis(scan_id)')

    @auto_heal
    def create_sensory_intelligence_db(self, db_path):
        """Create database for sensory data + AI analysis"""
        with sqlite3.connect(db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sensory_intelligence (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    sensor_type TEXT,
                    data_content TEXT,
                    ai_analysis TEXT,
                    significance_level INTEGER,
                    action_taken TEXT,
                    memory_pillar TEXT
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sensor_type ON sensory_intelligence(sensor_type)')

    @auto_heal
    async def perform_intelligent_ocr_scan(self, speak_results=True):
        """Perform complete intelligent OCR scan with dual AI analysis"""
        scan_start_time = time.time()
        scan_id = f"ocr_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🔍 Starting intelligent OCR scan: {scan_id}")
        
        # Step 1: 4-Monitor OCR Capture
        all_findings, significant_findings = self.ocr_system.process_4_monitor_ocr()
        
        # Step 2: Dual AI Analysis for significant findings
        ai_analysis_results = []
        
        for finding in significant_findings:
            if finding['text'] and len(finding['text'].strip()) > 10:
                print(f"🧠 AI analyzing monitor {finding['monitor']}...")
                
                # Perform dual AI analysis
                ai_result = await self.ai_analyzer.dual_analyze_ocr(finding['text'])
                ai_result['monitor_id'] = finding['monitor']
                ai_result['scan_id'] = scan_id
                ai_analysis_results.append(ai_result)
                
                # Save to EKM databases
                self.save_ai_decision_to_ekm(scan_id, finding, ai_result)
        
        # Step 3: Process AI results and determine actions
        voice_announcements = []
        high_priority_findings = []
        
        for ai_result in ai_analysis_results:
            if 'combined_insights' in ai_result:
                insights = ai_result['combined_insights']
                
                if insights.get('should_speak', False) and speak_results:
                    priority = insights.get('priority_level', 'low')
                    monitor_id = ai_result.get('monitor_id', 'unknown')
                    
                    if priority == 'urgent':
                        announcement = f"URGENT: Monitor {monitor_id} requires immediate attention!"
                        emotion = "urgent"
                    elif priority == 'high':
                        announcement = f"Important finding on monitor {monitor_id}."
                        emotion = "excited"
                    else:
                        announcement = f"Notable activity on monitor {monitor_id}."
                        emotion = "pleased"
                    
                    voice_announcements.append((announcement, emotion))
                    
                    if priority in ['urgent', 'high']:
                        high_priority_findings.append(ai_result)
        
        # Step 4: Voice announcements
        if voice_announcements and speak_results:
            # Summary announcement
            count = len(voice_announcements)
            urgent_count = len([a for a in voice_announcements if "URGENT" in a[0]])
            
            if urgent_count > 0:
                summary = f"Commander! {urgent_count} urgent findings detected!"
                summary_emotion = "urgent"
            elif count > 2:
                summary = f"Multiple significant findings detected across {count} monitors."
                summary_emotion = "excited"
            elif count > 0:
                summary = f"AI analysis complete. {count} significant findings."
                summary_emotion = "pleased"
            
            self.ocr_system.speak_with_emotion(summary, summary_emotion)
            
            # Individual announcements
            for announcement, emotion in voice_announcements:
                self.ocr_system.speak_with_emotion(announcement, emotion)
                time.sleep(0.5)  # Brief pause between announcements
        
        # Step 5: Update statistics
        scan_time = time.time() - scan_start_time
        self.intelligence_stats["total_scans"] += 1
        self.intelligence_stats["significant_findings"] += len(significant_findings)
        self.intelligence_stats["ai_analyses"] += len(ai_analysis_results)
        self.intelligence_stats["voice_announcements"] += len(voice_announcements)
        
        # Step 6: Save scan summary
        scan_summary = {
            "scan_id": scan_id,
            "timestamp": datetime.now().isoformat(),
            "total_time": scan_time,
            "monitors_scanned": len(all_findings),
            "significant_findings": len(significant_findings),
            "ai_analyses_performed": len(ai_analysis_results),
            "voice_announcements": len(voice_announcements),
            "high_priority_count": len(high_priority_findings)
        }
        
        self.scan_history.append(scan_summary)
        self.save_scan_to_sensory_ekm(scan_summary, high_priority_findings)
        
        print(f"✅ Intelligent OCR scan complete in {scan_time:.2f}s")
        print(f"📊 Found {len(significant_findings)} significant, {len(ai_analysis_results)} analyzed")
        
        return scan_summary, ai_analysis_results

    @auto_heal
    def save_ai_decision_to_ekm(self, scan_id, finding, ai_result):
        """Save AI decision to Master EKM"""
        try:
            db_path = Path(self.master_ekm_path) / "OCR_INTELLIGENCE_EKM" / "ocr_ai_decisions.db"
            
            with sqlite3.connect(db_path) as conn:
                # Extract decision data
                claude_decision = json.dumps(ai_result.get('claude', {}))
                chatgpt_decision = json.dumps(ai_result.get('chatgpt', {}))
                combined_insights = ai_result.get('combined_insights', {})
                
                conn.execute('''
                    INSERT INTO ai_decisions 
                    (scan_id, monitor_id, ocr_text, claude_decision, chatgpt_decision,
                     final_decision, significance_score, should_save, should_speak, reasoning)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    scan_id,
                    finding['monitor'],
                    finding['text'][:1000],  # Truncate for storage
                    claude_decision,
                    chatgpt_decision,
                    json.dumps(combined_insights),
                    combined_insights.get('final_significance', 1),
                    combined_insights.get('should_save', False),
                    combined_insights.get('should_speak', False),
                    ', '.join(combined_insights.get('combined_reasoning', []))
                ))
                
        except Exception as e:
            print(f"⚠️ EKM save error: {e}")

    @auto_heal
    def save_scan_to_sensory_ekm(self, scan_summary, high_priority_findings):
        """Save scan results to Sensory EKM"""
        try:
            db_path = Path(self.master_ekm_path) / "SENSORY_EKM" / "sensory_intelligence.db"
            
            with sqlite3.connect(db_path) as conn:
                conn.execute('''
                    INSERT INTO sensory_intelligence
                    (sensor_type, data_content, ai_analysis, significance_level, action_taken, memory_pillar)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    "4_monitor_ocr",
                    json.dumps(scan_summary),
                    json.dumps(high_priority_findings),
                    len(high_priority_findings) + 1,
                    f"voice_announcements:{scan_summary['voice_announcements']}",
                    "L3" if high_priority_findings else "L2"
                ))
                
        except Exception as e:
            print(f"⚠️ Sensory EKM save error: {e}")

    @auto_heal
    def start_auto_scanning(self, interval_seconds=30):
        """Start automatic intelligent scanning"""
        self.auto_scan_interval = interval_seconds
        self.auto_scan_enabled = True
        
        def auto_scan_loop():
            while self.auto_scan_enabled:
                try:
                    print(f"⏰ Auto scan triggered (every {self.auto_scan_interval}s)")
                    asyncio.run(self.perform_intelligent_ocr_scan(speak_results=True))
                    
                except Exception as e:
                    print(f"⚠️ Auto scan error: {e}")
                
                # Wait for next scan
                for _ in range(self.auto_scan_interval):
                    if not self.auto_scan_enabled:
                        break
                    time.sleep(1)
        
        # Start auto-scanning in background thread
        scan_thread = threading.Thread(target=auto_scan_loop, daemon=True)
        scan_thread.start()
        
        self.ocr_system.speak_with_emotion(
            f"Automatic intelligent scanning activated. Monitoring every {interval_seconds} seconds.", 
            "pleased"
        )
        
        print(f"🔄 Auto scanning started - every {interval_seconds} seconds")

    @auto_heal
    def stop_auto_scanning(self):
        """Stop automatic scanning"""
        self.auto_scan_enabled = False
        self.ocr_system.speak_with_emotion("Automatic scanning disabled.", "calm")
        print("🛑 Auto scanning stopped")

    @auto_heal
    def get_intelligence_stats(self):
        """Get current intelligence statistics"""
        stats = self.intelligence_stats.copy()
        stats['scan_history_count'] = len(self.scan_history)
        stats['average_findings_per_scan'] = (
            stats['significant_findings'] / max(1, stats['total_scans'])
        )
        return stats

    @auto_heal
    async def run_coordination_shell(self):
        """Interactive coordination shell"""
        print("🎯 OCR Intelligence Coordinator - Interactive Shell")
        print("Commands: scan, auto, stop, stats, voice, exit")
        
        while True:
            try:
                cmd = input("\n🎯 OCR> ").strip().lower()
                
                if cmd == "scan":
                    await self.perform_intelligent_ocr_scan(speak_results=True)
                    
                elif cmd == "auto":
                    interval = input("Auto scan interval (seconds, default 30): ").strip()
                    interval = int(interval) if interval.isdigit() else 30
                    self.start_auto_scanning(interval)
                    
                elif cmd == "stop":
                    self.stop_auto_scanning()
                    
                elif cmd == "stats":
                    stats = self.get_intelligence_stats()
                    print(json.dumps(stats, indent=2))
                    
                elif cmd == "voice":
                    text = input("Text to speak: ").strip()
                    emotion = input("Emotion (calm/excited/urgent/pleased): ").strip() or "calm"
                    self.ocr_system.speak_with_emotion(text, emotion)
                    
                elif cmd == "exit":
                    self.stop_auto_scanning()
                    break
                    
                else:
                    print("Commands: scan, auto, stop, stats, voice, exit")
                    
            except KeyboardInterrupt:
                print("\n🛑 Exiting coordination shell...")
                break
            except Exception as e:
                print(f"⚠️ Command error: {e}")

# Main execution
if __name__ == "__main__":
    async def main():
        coordinator = OCRIntelligenceCoordinator()
        
        # Start coordination shell
        await coordinator.run_coordination_shell()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 OCR Intelligence Coordinator stopped")
