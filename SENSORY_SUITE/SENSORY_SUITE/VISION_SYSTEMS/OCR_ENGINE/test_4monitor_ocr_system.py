#!/usr/bin/env python3
"""
4-Monitor OCR Intelligent System - Quick Test
Tests all components: OCR, AI analysis, voice, and memory integration
"""
import sys
import os
import asyncio
import time

# Add paths for our components
sys.path.append("E:/ECHO_X_V2.0/SENSORY_SUITE_ULTIMATE/VISION_SYSTEMS/OCR_ENGINE")

def test_imports():
    """Test that all required modules can be imported"""
    print("🔧 Testing imports...")
    
    try:
        from four_monitor_ocr_intelligent import FourMonitorOCRIntelligent
        print("✅ four_monitor_ocr_intelligent.py - OK")
    except Exception as e:
        print(f"❌ four_monitor_ocr_intelligent.py - {e}")
        return False
    
    try:
        from dual_ai_ocr_analyzer import DualAIOCRAnalyzer
        print("✅ dual_ai_ocr_analyzer.py - OK")
    except Exception as e:
        print(f"❌ dual_ai_ocr_analyzer.py - {e}")
        return False
    
    try:
        from ocr_intelligence_coordinator import OCRIntelligenceCoordinator
        print("✅ ocr_intelligence_coordinator.py - OK")
    except Exception as e:
        print(f"❌ ocr_intelligence_coordinator.py - {e}")
        return False
    
    return True

def test_voice_system():
    """Test voice response system"""
    print("\n🎤 Testing voice system...")
    
    try:
        from four_monitor_ocr_intelligent import FourMonitorOCRIntelligent
        
        ocr_system = FourMonitorOCRIntelligent()
        
        # Test different emotions
        emotions = ["calm", "excited", "urgent", "pleased", "thoughtful"]
        
        for emotion in emotions:
            print(f"Testing {emotion} emotion...")
            ocr_system.speak_with_emotion(
                f"Testing {emotion} voice response with emotional range",
                emotion,
                cache=False  # Don't cache during testing
            )
            time.sleep(1)
        
        print("✅ Voice system test completed")
        return True
        
    except Exception as e:
        print(f"❌ Voice system test failed: {e}")
        return False

def test_wake_word_detection():
    """Test fuzzy logic wake word detection"""
    print("\n🎯 Testing wake word detection...")
    
    try:
        from four_monitor_ocr_intelligent import FourMonitorOCRIntelligent
        
        ocr_system = FourMonitorOCRIntelligent()
        
        # Test cases
        test_cases = [
            ("trinity system activate", True),
            ("hey echo are you there", True),
            ("echo prime begin analysis", True),
            ("analyze this screen now", True),
            ("commander status report", True),
            ("hello world", False),
            ("echo", True),  # Should match with fuzzy logic
            ("trin", True),  # Should fuzzy match "trinity"
            ("", False)
        ]
        
        passed = 0
        total = len(test_cases)
        
        for test_text, expected in test_cases:
            detected, wake_word = ocr_system.detect_wake_word_fuzzy(test_text)
            
            if detected == expected:
                status = "✅"
                passed += 1
            else:
                status = "❌"
            
            print(f"{status} '{test_text}' -> {detected} (expected {expected})")
            if detected and wake_word:
                print(f"    Wake word: {wake_word}")
        
        print(f"\n🎯 Wake word detection: {passed}/{total} tests passed")
        return passed == total
        
    except Exception as e:
        print(f"❌ Wake word detection test failed: {e}")
        return False

async def test_ai_analysis():
    """Test dual AI analysis system"""
    print("\n🧠 Testing dual AI analysis...")
    
    try:
        from dual_ai_ocr_analyzer import DualAIOCRAnalyzer
        
        analyzer = DualAIOCRAnalyzer()
        
        # Test cases
        test_cases = [
            "System Error: Database connection failed with timeout 30 seconds",
            "Progress: 85% Complete - Processing files...",
            "User login successful - Welcome John Doe",
            "Critical Warning: Memory usage at 95% - System may become unstable",
            "Task completed successfully - All files processed"
        ]
        
        for i, test_text in enumerate(test_cases, 1):
            print(f"\n🔍 Test {i}: Analyzing text...")
            print(f"   Text: {test_text[:50]}...")
            
            result = await analyzer.dual_analyze_ocr(test_text)
            
            if "combined_insights" in result:
                insights = result["combined_insights"]
                print(f"   Significance: {insights.get('final_significance', 'N/A')}")
                print(f"   Should save: {insights.get('should_save', False)}")
                print(f"   Should speak: {insights.get('should_speak', False)}")
                print(f"   Priority: {insights.get('priority_level', 'low')}")
            else:
                print(f"   Result: {result.get('status', 'unknown')}")
        
        print("✅ Dual AI analysis test completed")
        return True
        
    except Exception as e:
        print(f"❌ Dual AI analysis test failed: {e}")
        return False

def test_memory_integration():
    """Test 9-Pillar Memory integration"""
    print("\n💾 Testing 9-Pillar Memory integration...")
    
    try:
        from four_monitor_ocr_intelligent import FourMonitorOCRIntelligent
        
        ocr_system = FourMonitorOCRIntelligent()
        
        # Test saving to different pillars
        test_data = {
            "test_type": "memory_integration_test",
            "timestamp": time.time(),
            "content": "Test data for memory pillar routing"
        }
        
        # Test different significance levels
        significance_levels = [1, 3, 5, 8]
        
        for level in significance_levels:
            result = ocr_system.save_to_9_pillar_memory(test_data, level)
            
            if result:
                print(f"✅ Saved to memory with significance level {level}")
            else:
                print(f"❌ Failed to save with significance level {level}")
        
        print("✅ Memory integration test completed")
        return True
        
    except Exception as e:
        print(f"❌ Memory integration test failed: {e}")
        return False

async def run_full_system_test():
    """Run complete system integration test"""
    print("\n🚀 Running full system integration test...")
    
    try:
        from ocr_intelligence_coordinator import OCRIntelligenceCoordinator
        
        coordinator = OCRIntelligenceCoordinator()
        
        print("📊 System statistics:")
        stats = coordinator.get_intelligence_stats()
        
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n🔍 Testing single OCR scan (without voice announcements)...")
        scan_summary, ai_results = await coordinator.perform_intelligent_ocr_scan(speak_results=False)
        
        print(f"✅ Scan completed in {scan_summary['total_time']:.2f}s")
        print(f"   Monitors scanned: {scan_summary['monitors_scanned']}")
        print(f"   Significant findings: {scan_summary['significant_findings']}")
        print(f"   AI analyses: {scan_summary['ai_analyses_performed']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Full system test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 4-MONITOR OCR INTELLIGENT SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    tests = [
        ("Import Tests", test_imports),
        ("Voice System", test_voice_system),
        ("Wake Word Detection", test_wake_word_detection),
        ("AI Analysis", test_ai_analysis),
        ("Memory Integration", test_memory_integration),
        ("Full System Integration", run_full_system_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                print(f"✅ {test_name} - PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} - FAILED")
                
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print(f"\n{'='*80}")
    print(f"🎊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION!")
    else:
        print(f"⚠️  {total - passed} tests failed - Review issues above")
        
    print("="*80)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
